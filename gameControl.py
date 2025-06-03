import chess
import chessEngine

initial_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" #base chessboard state
print("ran")
game = chessEngine.chessStatePy(initial_fen)
board = chess.Board()
bot1 = chessEngine.chessStatePy(initial_fen)
bot2 = chessEngine.chessStatePy(initial_fen)
turn = False
bots = [bot1, bot2]

cont = True
while(cont):
  botMove = bots[turn].searchMove()
  turn = not turn
  bots[turn].playerMove(botMove)
  board.push_uci(botMove)
  if(board.is_checkmate()):
    cont = False
    print("Checkmate")
  elif(board.can_claim_threefold_repetition()):
    cont = False
    print("Draw by three-fold")
  elif(board.is_stalemate()):
    cont = False
    print("Stalemate")
  elif(board.is_fifty_moves()):
    cont = False
    print("Draw by fifty move rule")    
  


  
