#include <stdio.h>
#include <dlfcn.h>

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <library> <function>\n", argv[0]);
        return 1;
    }
    
    char *library_path = argv[1];
    char *function_name = argv[2];
    
    void *handle = dlopen(library_path, RTLD_LAZY);
    if (!handle) {
        fprintf(stderr, "Error loading library: %s\n", dlerror());
        return 1;
    }
    
    void (*func)() = dlsym(handle, function_name);
    if (!func) {
        fprintf(stderr, "Error loading function: %s\n", dlerror());
        dlclose(handle);
        return 1;
    }
    
    // 调用函数
    func();
    
    dlclose(handle);
    return 0;
}
