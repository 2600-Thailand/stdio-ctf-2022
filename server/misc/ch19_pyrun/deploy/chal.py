blacklist = ["import", "upper", "lower", "open", "os", "system", "exit", "compile", "chr", "list", "__import__", "object", "assert", "__builtins__", "exec", "eval", "_", "\\", "hex", "encode", "decode"]

def check_blacklist(val):
    for keyword in blacklist:
        if keyword.lower() in val.lower():
            print("The command specified is not allowed!")
            return False

    return True

print("================= PyRun =================")
print("Feel free to run your Python code here :)")

while True:
    val = input('$ ')
    
    if check_blacklist(val):
        try:
            exec(val)
        except:
            print("?")
