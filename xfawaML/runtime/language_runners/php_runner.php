<?php
if ($argc < 2) {
    fwrite(STDERR, "Usage: php php_runner.php <script>\n");
    exit(1);
}

$script = $argv[1];

try {
    include $script;
} catch (Throwable $e) {
    fwrite(STDERR, "PHP execution error: " . $e->getMessage() . "\n");
    exit(1);
}
?>
