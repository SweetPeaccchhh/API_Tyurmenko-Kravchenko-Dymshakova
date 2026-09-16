from fastapi import FastAPI, HTTPException, Query

MAX_NUMBER = 1e15          # защита от гигантских чисел
LOG_LEVEL = "INFO"

app = FastAPI(
    title="Calculator API",
    description="Простой API-калькулятор: Тюрменко, Кравченко, Дымшакова",
    version="1.0.0",
)


@app.get("/")
def root():
    """Проверка статуса сервера """
    return {"status": "ok", "service": "calculator-api", "version": "1.0.0"}


@app.get("/add")
def add(a: float = Query(...), b: float = Query(...)):
    """Сложение: /add?a=2&b=3 (как будет отображаться)"""
    return {"operation": "add", "a": a, "b": b, "result": a + b}


@app.get("/sub")
def sub(a: float = Query(...), b: float = Query(...)):
    """Вычитание: /sub?a=5&b=2"""
    return {"operation": "sub", "a": a, "b": b, "result": a - b}


@app.get("/mul")
def mul(a: float = Query(...), b: float = Query(...)):
    """Умножение: /mul?a=4&b=3"""
    return {"operation": "mul", "a": a, "b": b, "result": a * b}


@app.get("/div")
def div(a: float = Query(...), b: float = Query(...)):
    """Деление: /div?a=10&b=2"""
    if b == 0:
        raise HTTPException(status_code=400, detail="Деление на ноль невозможно")
    return {"operation": "div", "a": a, "b": b, "result": a / b}


@app.get("/health")
def health():
    """Проверки здоровья для Docker и Пайплайн"""
    return {"status": "healthy"}

# ---------- Расширенные операции ----------

def check(value: float) -> float:
    """Проверяет, что число не слишком большое."""
    if abs(value) > MAX_NUMBER:
        raise HTTPException(
            status_code=422,
            detail={"code": "number_too_large", "message": f"Число превышает {MAX_NUMBER}"},
        )
    return value

def ok(operation: str, result: float, a: float, b: float | None = None) -> dict:
    """Единый формат успешного ответа."""
    response = {"operation": operation, "a": a, "result": result}
    if b is not None:
        response["b"] = b
    return response

@app.get("/v1/pow", tags=["advanced"])
def pow_(a: float = Query(...), b: float = Query(...)):
    return ok("pow", check(a ** b), a, b)


@app.get("/v1/sqrt", tags=["advanced"])
def sqrt(a: float = Query(...)):
    if a < 0:
        raise HTTPException(
            status_code=422,
            detail={"code": "negative_sqrt", "message": "Корень из отрицательного числа не определён"},
        )
    return ok("sqrt", check(a ** 0.5), a)


@app.get("/v1/mod", tags=["advanced"])
def mod(a: float = Query(...), b: float = Query(...)):
    if b == 0:
        raise HTTPException(
            status_code=400,
            detail={"code": "division_by_zero", "message": "Остаток от деления на ноль не определён"},
        )
    return ok("mod", a % b, a, b)

