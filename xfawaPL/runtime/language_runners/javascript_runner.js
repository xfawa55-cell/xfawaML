const { spawn } = require('child_process');

function runJavaScript(filePath) {
    return new Promise((resolve, reject) => {
        const node = spawn('node', [filePath]);
        
        let stdout = '';
        let stderr = '';
        
        node.stdout.on('data', (data) => {
            stdout += data.toString();
        });
        
        node.stderr.on('data', (data) => {
            stderr += data.toString();
        });
        
        node.on('close', (code) => {
            if (code !== 0) {
                reject(new Error(`JavaScript execution failed with code ${code}: ${stderr}`));
            } else {
                resolve(stdout);
            }
        });
    });
}

// 主执行逻辑
if (process.argv.length < 3) {
    console.error('Usage: node javascript_runner.js <script>');
    process.exit(1);
}

const scriptPath = process.argv[2];
runJavaScript(scriptPath)
    .then(output => console.log(output))
    .catch(err => {
        console.error(err.message);
        process.exit(1);
    });
