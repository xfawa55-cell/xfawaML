#include <iostream>
#include <dlfcn.h>

int main(int argc, char *argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <library> <function>" << std::endl;
        return 1;
    }
    
    char *library_path = argv[1];
    char *function_name = argv[2];
    
    void *handle = dlopen(library_path, RTLD_LAZY);
    if (!handle) {
        std::cerr << "Error loading library: " << dlerror() << std::endl;
        return 1;
    }
    
    void (*func)() = (void (*)())dlsym(handle, function_name);
    if (!func) {
        std::cerr << "Error loading function: " << dlerror() << std::endl;
        dlclose(handle);
        return 1;
    }
    
    // 调用函数
    func();
    
    dlclose(handle);
    return 0;
}
