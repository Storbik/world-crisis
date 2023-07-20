from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_items():
    with open('index.html', encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

# Список для хранения всех подключенных WebSocket клиентов
connected_clients: List[WebSocket] = []


# WebSocket endpoint для подключения
@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            # Здесь можно обрабатывать полученные данные, если это необходимо
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        print("WebSocket client disconnected.")
        

# Мониторинг подключенных пользователей
@app.on_event("startup")
async def startup_event():
    print("Server started and running.")

@app.on_event("shutdown")
async def shutdown_event():
    print("Server stopped.")
    for client in connected_clients:
        try:
            await client.close()
        except Exception as e:
            print(f"Error while closing WebSocket: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)