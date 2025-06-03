import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import sys
import datetime
try:
  import chessEngine
  import chess
except:
  print("Engine failed to load")
  sys.exit()

load_dotenv()
botToken = os.getenv("DISCORD_TOKEN")
owner = int(os.getenv("YOUR_DISCORD_ID"))
intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='!', intents=intents)
active = False
initial_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" #base chessboard state
player = None
game = None
board = None
channel = None #reused globals, player marks user, game holds chessState object, board holds chess object, channel

timeout = 180
lastPrompt = None

def endCond(state: chess.Board):
  if(state.is_checkmate()):
    return "Checkmate"
  elif(state.is_fifty_moves()):
    return "Fifty-move draw"
  elif(state.can_claim_threefold_repetition()):
    return "Threefold"
  elif(state.is_stalemate()):
    return "Stalemate"
  elif(state.is_fivefold_repetition()):
    return "Fivefold repetition"
  else:
    return "C"

#resets globals
def endGame(): 
  global player
  global game
  global board
  global channel
  global active 
  global lastPrompt

  board = None 
  game = None
  player = None
  channel = None
  active = False
  lastPrompt = None
  checkTimeout.cancel()   

#forms string representation of board
def makeBoard():
  board = "  -------------------------------------\n"
  for i in range(7, -1, -1):
    board += f"{i+1} |"
    for j in range(0, 8, 1):
      board += f"{game.pieceAt(i*8 + j)} | "
    board += "\n  -------------------------------------\n"
  board += "   a      b      c      d      e      f      g      h\n"
  return board

@tasks.loop(seconds=30)
async def checkTimeout():
  print("checking")
  global active
  channel
  player
  lastPrompt
  timeout
  if active and lastPrompt is not None:
    timeGap = datetime.datetime.now() - lastPrompt
    print(timeGap.total_seconds())
    if timeGap.total_seconds() >= timeout:
      await channel.send(f"{player.mention} you have timed out, the game is closed")
      endGame()

@bot.event
async def on_ready():
  print(f'{bot.user} logged in\n')

#initializes a chess game
@bot.command(name='play')
async def initialize(ctx):
  print("initiated")
  global active
  if active == True:
    await ctx.channel.send("Game already active")
    return
  await ctx.channel.send("Starting game")
  checkTimeout.start()
  global player
  global game
  global board
  global channel
  global lastPrompt

  active = True
  player = ctx.author
  game = chessEngine.chessStatePy(initial_fen)
  board = chess.Board()
  channel = ctx.channel
  
  toSend = "Game start, bot moves first\n"
  toSend += makeBoard()
  await channel.send(toSend)
  try:
    botMove = game.searchMove()
    await channel.send(f"Bot moves {botMove}")
    board.push_uci(botMove)
    toSend = makeBoard()
    toSend += "Legal moves: "
  except:
    toSend = "Bot failed to move, ending"
    endGame()
  legalMoves = []
  for iter in board.legal_moves:
    legalMoves.append(board.uci(iter))
  legalMoves.sort()
  toSend += legalMoves[0]
  legalMoves.pop(0)
  for l in legalMoves:
    toSend += f", {l}"
  await channel.send(toSend)
  lastPrompt = datetime.datetime.now()


@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  global player
  global game
  global board
  global channel
  global lastPrompt
  print("a")

  if(active == False):
    await bot.process_commands(message)
    return
  elif(channel != message.channel):
    await bot.process_commands(message)
    return
  elif(message.author != player):
    await bot.process_commands(message)
    return
  move = message.content
  lastPrompt = datetime.datetime.now()
  try:
    board.push_uci(move)
  except:
    await channel.send("Invalid move")
    return
  game.playerMove(move)
  status = endCond(board)
  toSend = makeBoard()
  if(status == "Checkmate"):
    toSend += "You win by checkmate"
    await message.channel.send(toSend)
    endGame()
    return
  if(status == "Fivefold repetition"):
    toSend += "Draw by fivefold repetition"
    await message.channel.send(toSend)
    endGame()
    return
  if(status == "Stalemate"):
    toSend += "Stalemate"
    await message.channel.send(toSend)
    endGame()
    return
  if(status == "Fifty-move draw"):
    toSend += "Draw by fifty-move rule"
    await message.channel.send(toSend)
    endGame()
    return
  await message.channel.send(toSend)

  botMove = game.searchMove()
  try:
    board.push_uci(botMove)
    await channel.send(f"Bot moves {botMove}")
  except:
    await channel.send("Bot made an invalid move, resetting")
    endGame()
    return
  
  status = endCond(board)
  toSend = makeBoard()
  if(status == "Checkmate"):
    toSend += "Bot win by checkmate"
    await message.channel.send(toSend)
    endGame()
    return
  if(status == "Fivefold repetition"):
    toSend += "Draw by fivefold repetition"
    await message.channel.send(toSend)
    endGame()
    return
  if(status == "Stalemate"):
    toSend += "Stalemate"
    await message.channel.send(toSend)
    endGame()
    return
  if(status == "Fifty-move draw"):
    toSend += "Draw by fifty-move rule"
    await message.channel.send(toSend)
    endGame()
    return
  elif(status == "Threefold"): #implement later
    toSend += "You may force a draw due to three-fold repetition"
  i = 0
  legalMoves = []
  for iter in board.legal_moves:
    legalMoves.append(board.uci(iter))
  legalMoves.sort()
  toSend += f"Legal moves: {legalMoves[0]}"
  legalMoves.pop(0)
  for l in legalMoves:
    toSend += f", {l}"
  await message.channel.send(toSend)
  lastPrompt = datetime.datetime.now()

bot.run(botToken) 