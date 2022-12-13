import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import app.core.database as DBCall

DBCall.init()

class Req_Add(BaseModel):
  number: int

class Resp_Add(BaseModel):
  message: str
  number: int

class Resp_Sample(BaseModel):
  success: bool
  samples: list

class Resp_Clear(BaseModel):
  success: bool

app = FastAPI()

@app.post("/add")
async def add_post(req: Req_Add):
  input = req.number
  if DBCall.add(input):
    return Resp_Add(message="added!", number=input)
  else:
    return Resp_Add(message="duplicate number!", number=input)
  
@app.get("/sample10")
async def sample10():
  output = DBCall.random_sample10()
  if output:
    return Resp_Sample(success=True, samples=output)
  else:
    return Resp_Sample(success=False, samples=output)

@app.get("/clear")
async def clear():
  return Resp_Clear(success=DBCall.clear())

if __name__ == "__main__":
  config = uvicorn.Config("main:app", port=80, log_level="info")
  server = uvicorn.Server(config)
  server.run()
  DBCall.cur.close()
  DBCall.conn.close()