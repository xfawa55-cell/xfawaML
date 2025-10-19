import java.lang.reflect.Method;

public class JavaRunner {
    public static void main(String[] args) {
        if (args.length != 2) {
            System.err.println("Usage: JavaRunner <class> <method>");
            System.exit(1);
        }
        
        String className = args[0];
        String methodName = args[1];
        
        try {
            Class<?> cls = Class.forName(className);
            Method method = cls.getDeclaredMethod(methodName);
            Object instance = cls.getDeclaredConstructor().newInstance();
            Object result = method.invoke(instance);
            System.out.println(result);
        } catch (Exception e) {
            System.err.println("Java runner error: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
    }
}
