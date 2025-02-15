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
        
        # 动态生成中文分类映射
        self.CATEGORY_MAP = self._generate_category_map()

    def _load_regex_library(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _generate_category_map(self):
        """动态生成分类映射"""
        base_map = {
        }
        
        # 从正则库中获取所有pattern名称
        for pattern_name in self.regex_library.keys():
            if pattern_name not in base_map:
                # 对于未定义映射的pattern,使用pattern名称本身
                base_map[pattern_name] = pattern_name.replace('_', ' ').title()
                
        return base_map

    def scan_directory(self, directory):
        start_time = datetime.now()
        if not os.path.exists(directory):
            os.makedirs(directory)

        for dirpath, _, filenames in os.walk(directory):
            self.summary['total_files'] += len(filenames)
            for file in filenames:
                self._scan_file(os.path.join(dirpath, file), file)

        self.summary['scan_time'] = (datetime.now() - start_time).total_seconds()

    def _scan_file(self, file_path, file_name):
        try:
            with open(file_path, "r", encoding='utf-8', errors='ignore') as f:
                content = f.read()
                self._process_content(file_name, content)
        except Exception as e:
            print(f"Error processing file {file_name}: {str(e)}")

    def _process_content(self, file, content):
        """处理文件内容"""
        # 处理正则库中的模式
        for regex_name, regex_pattern in self.regex_library.items():
            if isinstance(regex_pattern, dict):  # 跳过嵌套模式
                continue
            
            try:
                matches = re.finditer(regex_pattern, content, re.MULTILINE | re.DOTALL)
                unique_matches = set()
                
                for match in matches:
                    match_str = match.group(0)
                    if not match_str.strip():  # 跳过空匹配
                        continue
                        
                    start_pos = match.start()
                    
                    # HTML转义并保持换行格式
                    match_str = html.escape(match_str)
                    match_str = match_str.replace('\n', '<br>')
                    
                    if match_str not in unique_matches:
                        unique_matches.add(match_str)
                        line_number = content.count('\n', 0, start_pos) + 1
                        
                        category = self.CATEGORY_MAP.get(regex_name, regex_name)
                        self.results[category][file].append({
                            'line_number': line_number,
                            'match': match_str,
                        })
                        self.summary['total_matches'] += 1
                        self.summary['patterns_matched'][category] += 1
            except Exception as e:
                print(f"Error processing pattern {regex_name}: {str(e)}")

    def convert_to_frontend_format(self):
        """转换数据格式以匹配前端需求"""
        frontend_data = {}
        
        for category, files in self.results.items():
            if not files:  # 跳过空结果
                continue
                
            frontend_data[category] = []
            for file_name, matches in files.items():
                for match in matches:
                    frontend_data[category].append({
                        "fileName": file_name,
                        "lineNumber": match["line_number"],
                        "content": match["match"]
                    })
        
        # 添加调试输出
        
        return frontend_data

    def generate_report(self, output_file):
        """生成HTML报告"""
        frontend_data = self.convert_to_frontend_format()
        
        if not frontend_data:
            print("Warning: No matches found!")
            frontend_data = {"未发现敏感信息": []}
        
        # 读取模板文件
        template_path = os.path.join(os.path.dirname(__file__), 'mould.html')
        with open(template_path, 'r', encoding='utf-8') as template:
            html_content = template.read()
        
        # 查找模板中的数据注入点
        start_marker = 'const sensitiveInfoReport = {'
        end_marker = '})'
        
        # 构造要注入的数据字符串
        data_injection = f'const sensitiveInfoReport = {json.dumps(frontend_data, ensure_ascii=False, indent=2)}'
        
        # 在模板中定位并替换示例数据
        start_idx = html_content.find(start_marker)
        if start_idx == -1:
            raise ValueError("Could not find data injection point in template")
        
        end_idx = html_content.find(end_marker, start_idx)
        if end_idx == -1:
            raise ValueError("Could not find end of data section in template")
        
        # 替换整个数据部分
        new_html_content = (
            html_content[:start_idx] + 
            data_injection + 
            html_content[end_idx + len(end_marker):]
        )
        
        # 写入输出文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(new_html_content)

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
