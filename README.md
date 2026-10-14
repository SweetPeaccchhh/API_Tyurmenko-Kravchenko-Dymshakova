ЭТАП 4
Для демонстрации работы сканеров безопасности были добавлены следующие сроки:
1) в файл main.py: фейковый секрет (для показа работы Gitleaks):
"from fastapi import FastAPI, HTTPException, Query
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
STRIPE_API_KEY = "sk_live_**DEMO***"

MAX_NUMBER = 1e15          # защита от гигантских чисел
LOG_LEVEL = "INFO"
..."
И добавляем небезопасный эндпоинт (для показа работы Bandit):
"...
@app.get("/v2/calc", tags=["unsafe"])
def unsafe_calc(expression: str = Query(...)):
    """
    Используем eval() (опасно)
    Позволяет выполнить любой Python-код.
    """
    try:
        result = eval(expression)   # ОПАСНО: B307 от Bandit
        return {"expression": expression, "result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))"

2) в файл requirements:
"...
requests==2.19.0" для демонстрации работы для Trivy (устаревшая библиотека requests)

После этого github заблокировал пуш:
<img width="817" height="466" alt="image" src="https://github.com/user-attachments/assets/b2ac56e3-99c3-4776-a8a0-c99806c6f170" />
<img width="1337" height="749" alt="image" src="https://github.com/user-attachments/assets/a423666d-f27a-4669-976c-276387f0eb4a" />

Локально сработал: Gitleaks (через Docker), который был установлен командой: docker run zricethezav/gitleaks
А также Gitleaks (в workflow): gitleaks/gitleaks-action@v2
