package main

import (
	"fmt"
	"os"
	"plugin"
)

func main() {
	if len(os.Args) != 3 {
		fmt.Fprintf(os.Stderr, "Usage: %s <plugin> <function>\n", os.Args[0])
		os.Exit(1)
	}

	pluginPath := os.Args[1]
	functionName := os.Args[2]

	// 加载插件
	p, err := plugin.Open(pluginPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error loading plugin: %v\n", err)
		os.Exit(1)
	}

	// 查找函数
	sym, err := p.Lookup(functionName)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error looking up symbol: %v\n", err)
		os.Exit(1)
	}

	// 类型断言为函数
	fn, ok := sym.(func())
	if !ok {
		fmt.Fprintf(os.Stderr, "Symbol is not a function\n")
		os.Exit(1)
	}

	// 调用函数
	fn()
}
