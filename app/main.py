from flask import Flask, request, jsonify
import subprocess  # Add this line
import json


app = Flask(__name__)

# def execute_script(script):
#     try:
#         result = subprocess.run(
#             ["nsjail", "--config", "nsjail.cfg", "--", "/usr/local/bin/python3", "-c", script],
#             capture_output=True,
#             text=True,
#             timeout=5
#         )
#         if result.returncode != 0:
#             return None, result.stderr.strip()
#         return result.stdout.strip(), None
#     except Exception as e:
#         return None, str(e)
def execute_script(script):
    # Wrap the script to make sure it includes the full Python structure
    full_script = f"""
{script}
print(main())
"""

    try:
        # Use nsjail to run the script in a restricted environment
        result = subprocess.run(
            ["nsjail", "--config", "nsjail.cfg", "--", "/usr/local/bin/python3", "-c", full_script],
            capture_output=True,
            text=True,
            timeout=5
        )

        # Print output for debugging
        print("Debug stdout:", result.stdout)
        print("Debug stderr:", result.stderr)

        # Return appropriate response based on execution results
        if result.returncode != 0:
            return None, result.stderr.strip()
        return result.stdout.strip(), None
    except Exception as e:
        return None, str(e)

@app.route('/execute', methods=['POST'])
def execute():
    data = request.get_json()

    if "script" not in data:
        return jsonify({"error": "Missing script field in JSON"}), 400

    script = data["script"]

    # Ensure main() function exists
    if "def main()" not in script:
        return jsonify({"error": "Script must contain a main() function"}), 400

    output, error = execute_script(script)
    print("Debugging Output:", output)

    if error:
        return jsonify({"error": error}), 500

    # Attempt to parse the output as JSON
    try:
        # The output is expected to be a dictionary-like string
        result_json = eval(output) if isinstance(output, str) else output
        return jsonify({"result": result_json, "stdout": ""})
    except Exception:
        return jsonify({"error": "main() function must return a valid JSON"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
