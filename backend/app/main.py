from fastapi import FastAPI, HTTPException, status

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Laboratório distribuído funcionando!"}


@app.get("/is-even/{number}")
def is_even(number: int):
    if isinstance(number, str):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Não é possivel verificar paridade de string",
        )

    if isinstance(number, float):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Não é possivel verificar paridade de decimais",
        )

    result = number % 2 == 0
    return {"result": result}
