from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
WIN = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

def winner(b):
    for a,c,d in WIN:
        if b[a] == b[c] == b[d] and b[a] != " ":
            return b[a]
    return None

def minimax(b, is_ai, alpha, beta):
    w = winner(b)
    if w == "O": return 1
    if w == "X": return -1
    if " " not in b: return 0
    if is_ai:
        best = -float("inf")
        for i in range(9):
            if b[i] == " ":
                b[i] = "O"
                best = max(best, minimax(b, False, alpha, beta))
                b[i] = " "
                alpha = max(alpha, best)
                if beta <= alpha: break
        return best
    best = float("inf")
    for i in range(9):
        if b[i] == " ":
            b[i] = "X"
            best = min(best, minimax(b, True, alpha, beta))
            b[i] = " "
            beta = min(beta, best)
            if beta <= alpha: break
    return best

def ai_move(b):
    best, move = -float("inf"), None
    for i in range(9):
        if b[i] == " ":
            b[i] = "O"
            score = minimax(b, False, -float("inf"), float("inf"))
            b[i] = " "
            if score > best:
                best, move = score, i
    if move is not None:
        b[move] = "O"

@app.route("/", methods=["GET", "POST"])
def index():
    board = [" "] * 9
    if request.method == "POST":
        board = request.form.get("board", "         ")[:9].ljust(9)
        move = request.form.get("move")
        if move is not None and move.isdigit():
            i = int(move)
            if 0 <= i < 9 and board[i] == " " and not winner(board):
                board = list(board)
                board[i] = "X"
                if not winner(board) and " " in board:
                    ai_move(board)
        board = list(board)
    result = winner(board)
    if result == "X": message = "You win!"
    elif result == "O": message = "AI wins!"
    elif " " not in board: message = "It's a draw!"
    else: message = "Your turn (X)"
    return render_template("index.html", board=board, message=message)

@app.route("/reset")
def reset():
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
