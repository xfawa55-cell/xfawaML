if ARGV.length < 1
  $stderr.puts "Usage: ruby ruby_runner.rb <script>"
  exit 1
end

script = ARGV[0]

begin
  load script
rescue => e
  $stderr.puts "Ruby execution error: #{e.message}"
  exit 1
end
