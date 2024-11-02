import re
import os
import html
import json
from datetime import datetime
from collections import defaultdict
from urllib.parse import urlparse



class RegexMatcher():
    def __init__(self, regex_file):
        self.regex_library = self._load_regex_library(regex_file)
        self.results = defaultdict(lambda: defaultdict(list))
        self.summary = {
            'total_files': 0,
            'total_matches': 0,
            'patterns_matched': defaultdict(int),
            'scan_time': None
        }

    def _load_regex_library(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def scan_directory(self, directory):
        start_time = datetime.now()
        if not os.path.exists(directory):
            os.makedirs(directory)

        for dirpath, _, filenames in os.walk(directory):
            self.summary['total_files'] += len(filenames)
            for file in filenames:
                self._scan_file(directory, file)

        self.summary['scan_time'] = (datetime.now() - start_time).total_seconds()

    def _scan_file(self, directory, file):
        try:
            with open(os.path.join(directory, file), "r", encoding='utf-8', errors='ignore') as f:
                content = f.read()
                self._process_content(file, content)
        except Exception as e:
            print(f"Error processing file {file}: {str(e)}")

    def _process_content(self, file, content):
        # 处理注释的特殊模式
        comment_patterns = {
            'single_line_comment': r'//[^\n]*',
            'html_comment': r'<!--[\s\S]*?-->',
            'multiline_comment': r'/\*[\s\S]*?\*/',
            'single_line_c_style_comment': r'/\*[^\n]*\*/'
        }

        # 处理注释模式
        for comment_type, pattern in comment_patterns.items():
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                match_str = match.group(0)
                start_pos = match.start()
                
                # 检查是否应该跳过这个匹配
                should_skip = False
                if comment_type == 'single_line_c_style_comment' and '\n' in match_str:
                    should_skip = True
                if comment_type == 'multiline_comment' and '\n' not in match_str:
                    should_skip = True

                if not should_skip:
                    line_number = content.count('\n', 0, start_pos) + 1
                    match_str = html.escape(match_str)
                    match_str = match_str.replace('\n', '<br>')
                    
                    self.results[comment_type][file].append({
                        'line_number': line_number,
                        'match': match_str,
                    })
                    self.summary['total_matches'] += 1
                    self.summary['patterns_matched'][comment_type] += 1

        # 处理正则库中的其他模式
        for regex_name, regex_pattern in self.regex_library.items():
            if isinstance(regex_pattern, dict):  # Skip nested patterns
                continue
            
            matches = re.finditer(regex_pattern, content, re.MULTILINE | re.DOTALL)
            unique_matches = set()
            
            for match in matches:
                match_str = match.group(0)
                start_pos = match.start()
                
                # HTML转义并保持换行格式
                match_str = html.escape(match_str)
                match_str = match_str.replace('\n', '<br>')
                
                if match_str not in unique_matches:
                    unique_matches.add(match_str)
                    line_number = content.count('\n', 0, start_pos) + 1
                    
                    self.results[regex_name][file].append({
                        'line_number': line_number,
                        'match': match_str,
                    })
                    self.summary['total_matches'] += 1
                    self.summary['patterns_matched'][regex_name] += 1

    def generate_report(self, output_file):
            pattern_summary = "".join(
                f"<li>{pattern.replace('_', ' ').title()}: {count} matches</li>"
                for pattern, count in self.summary['patterns_matched'].items()
            )

            match_results = ""
            
            comment_types = ['single_line_comment', 'multiline_comment', 'html_comment']
            for regex_name in comment_types:
                if regex_name in self.results:
                    display_name = regex_name.replace('_', ' ').title()
                    match_results += self._generate_result_section(regex_name, display_name)

            for regex_name, files in self.results.items():
                if regex_name not in comment_types:
                    display_name = regex_name.replace('_', ' ').title()
                    match_results += self._generate_result_section(regex_name, display_name)

            html_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Pattern Match Report</title>
                <style>
                    body {{ font-family: Arial, sans-serif; background-color: #f0f2f5; color: #333; margin: 0; padding: 20px; }}
                    .container {{ max-width: 900px; margin: auto; padding: 20px; background: #fff; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); }}
                    h1 {{ text-align: center; font-size: 1.8em; color: #4a90e2; }}
                    h2 {{ font-size: 1.4em; color: #333; margin-top: 30px; }}
                    .summary {{ background-color: #e6f7ff; padding: 15px; border: 1px solid #b3e5ff; border-radius: 5px; margin-bottom: 20px; color: #005b99; }}
                    .summary h3 {{ margin-top: 0; font-size: 1.2em; }}
                    table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
                    th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #eee; }}
                    th {{ background-color: #4a90e2; color: white; font-weight: bold; }}
                    tr:hover {{ background-color: #f9f9f9; }}
                    .toggle-btn {{ cursor: pointer; padding: 10px; font-size: 16px; color: #005b99; background-color: #f0f2f5; border: none; text-align: left; width: calc(100% - 120px); outline: none; transition: background-color 0.3s; border-radius: 5px; margin-top: 10px; display: inline-block; }}
                    .toggle-btn:hover {{ background-color: #e6f7ff; }}
                    .match-details {{ display: none; max-height: 300px; overflow-y: auto; border-top: 1px solid #ddd; margin-top: 5px; }}
                    .match-content {{ white-space: pre-wrap; font-family: monospace; }}
                    .copy-btn {{ cursor: pointer; padding: 10px; font-size: 14px; color: white; background-color: #4a90e2; border: none; border-radius: 5px; margin-left: 10px; transition: background-color 0.3s; }}
                    .copy-btn:hover {{ background-color: #357abd; }}
                    .button-container {{ display: flex; align-items: center; }}
                    .success-message {{ color: green; margin-left: 10px; display: none; }}
                </style>
                <script>
                    function toggleDetails(regexName) {{
                        var details = document.getElementById("details-" + regexName);
                        if (details.style.display === "none" || !details.style.display) {{
                            details.style.display = "block";
                        }} else {{
                            details.style.display = "none";
                        }}
                    }}
                    
                    function copyResults(regexName) {{
                        var table = document.getElementById("details-" + regexName);
                        var rows = table.getElementsByTagName("tr");
                        var text = "";
                        
                        // Skip header row, only collect match content
                        for (var i = 1; i < rows.length; i++) {{
                            var cells = rows[i].getElementsByTagName("td");
                            // Only add the match content (third column)
                            text += cells[2].textContent + "\\n";
                        }}
                        
                        // Create temporary textarea to copy text
                        var textarea = document.createElement("textarea");
                        textarea.value = text;
                        document.body.appendChild(textarea);
                        textarea.select();
                        document.execCommand("copy");
                        document.body.removeChild(textarea);
                        
                        // Show success message
                        var successMsg = document.getElementById("success-" + regexName);
                        successMsg.style.display = "inline";
                        setTimeout(function() {{
                            successMsg.style.display = "none";
                        }}, 2000);
                    }}
                </script>
            </head>
            <body>
                <div class="container">
                    <h1>Pattern Match Report</h1>
                    <p style="text-align: center; font-size: 0.9em; color: #888;">Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    
                    <h2>Match Results</h2>
                    <div>
                        {match_results}
                    </div>
                </div>
            </body>
            </html>
            """

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

    def _generate_result_section(self, regex_name, display_name):
            """生成单个结果部分的HTML"""
            if regex_name not in self.results:
                return ""
                
            result = f"""
                <div class="button-container">
                    <button class="toggle-btn" onclick="toggleDetails('{regex_name}')">
                        {display_name} - {self.summary['patterns_matched'][regex_name]} matches
                    </button>
                    <button class="copy-btn" onclick="copyResults('{regex_name}')">Copy Matches</button>
                    <span id="success-{regex_name}" class="success-message">Copied!</span>
                </div>
                <div id="details-{regex_name}" class="match-details">
                    <table>
                        <tr>
                            <th>File</th>
                            <th>Line Number</th>
                            <th>Match</th>
                        </tr>
            """
            
            for file, matches in self.results[regex_name].items():
                for match in matches:
                    result += f"""
                        <tr>
                            <td>{file}</td>
                            <td>{match['line_number']}</td>
                            <td class="match-content">{match['match']}</td>
                        </tr>
                    """
            result += "</table></div>"
            return result
