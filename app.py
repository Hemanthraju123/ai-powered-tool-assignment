
from flask import Flask, request, jsonify
import cProfile
import io
import pstats
from contextlib import redirect_stdout

app = Flask(__name__)

# Analyze performance of the code
def analyze_code(code):
    # Simulate profiling of the code snippet
    profiler = cProfile.Profile()
    profiler.enable()

    try:
        exec(code)  # Execute the code to profile it
    except Exception as e:
        return str(e)

    profiler.disable()
    s = io.StringIO()
    with redirect_stdout(s):
        stats = pstats.Stats(profiler, stream=s)
        stats.sort_stats('cumulative')
        stats.print_stats()
    
    return s.getvalue()

# Endpoint to handle code analysis
@app.route('/upload', methods=['POST'])
def upload_code():
    if 'code' not in request.form:
        return jsonify({"error": "No code provided"}), 400
    
    code = request.form['code']
    analysis_result = analyze_code(code)
    
    # Simple optimization suggestions (AI could improve this later)
    suggestions = generate_suggestions(code)

    return jsonify({
        "analysis": analysis_result,
        "suggestions": suggestions
    })

def generate_suggestions(code):
    # This is a simple static list, but it could be enhanced with AI-based suggestions
    suggestions = []
    if 'for' in code and 'range' in code:
        suggestions.append("Consider using list comprehensions or generator expressions for better performance.")
    if 'open(' in code and 'read' in code:
        suggestions.append("Consider using 'with open' for automatic resource management.")
    if 'while' in code:
        suggestions.append("Check if a 'for' loop would be more efficient for iteration.")
    return suggestions

if __name__ == '__main__':
    app.run(debug=True)
