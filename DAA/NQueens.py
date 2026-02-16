import streamlit as st
import time

def safe(board, row, col, n):
    # Check the column
    for i in range(row):
        if board[i][col] == 1:
            return False
    # Check upper left diagonal
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False
    # Check upper right diagonal
    for i, j in zip(range(row, -1, -1), range(col, n, 1)):  # Fixed step size
        if j < n and board[i][j] == 1:
            return False
    return True

def solve_nqueen(board, row, n, solutions, progress):
    if row == n:
        solutions.append([r[:] for r in board])  # Store board, not row
        progress.append([r[:] for r in board])   # Store progress
        return
    for col in range(n):
        if safe(board, row, col, n):
            board[row][col] = 1
            progress.append([r[:] for r in board])  # Store board state
            solve_nqueen(board, row + 1, n, solutions, progress)
            board[row][col] = 0  # Backtrack
            progress.append([r[:] for r in board])  # Store backtrack step

def display_solution(solution):
    return "<br>".join(" ".join("♛" if cell else "⬜" if (i + j) % 2 == 0 else "⬛" for j, cell in enumerate(row)) for i, row in enumerate(solution))

st.title("♛ N-Queens Solver")

n = st.number_input("Enter the value of N:", min_value=4, step=1)

if "solutions" not in st.session_state or "progress" not in st.session_state or st.session_state.get("last_n") != n:
    st.session_state.solutions = []
    st.session_state.progress = []
    board = [[0] * n for _ in range(n)]
    solve_nqueen(board, 0, n, st.session_state.solutions, st.session_state.progress)
    st.session_state.last_n = n

st.session_state.view_mode = st.radio("Select View Mode", ["Solving Process", "Solutions"])

col1, col2 = st.columns(2)

if st.session_state.view_mode == "Solving Process":
    with col1:
        st.header("🔄 Solving Process")
        if st.session_state.progress:
            for idx, step in enumerate(st.session_state.progress, 1):
                st.markdown(f"**Step {idx}:**")
                st.markdown(display_solution(step), unsafe_allow_html=True)
                time.sleep(0.1)  # Optional
                st.rerun() # Updates the UI
        else:
            st.error("No solving process available! Try a different N value.")

elif st.session_state.view_mode == "Solutions":
    with col2:
        st.header("✅ Solutions")
        if st.session_state.solutions:
            st.write(f"Total Solutions: {len(st.session_state.solutions)}")
            for idx, solution in enumerate(st.session_state.solutions, 1):
                st.markdown(f"**Solution {idx}:**")
                st.markdown(display_solution(solution), unsafe_allow_html=True)
        else:
            st.error("No solutions found! Try a different N value.")
