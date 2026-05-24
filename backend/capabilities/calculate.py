def calculate(expression):
    try:
        result = eval(expression)        
        return result
    except Exception as e:
        print("❌ Calculation failed")
        print(e)