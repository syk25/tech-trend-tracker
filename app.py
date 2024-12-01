from flask import Flask, request, render_template
import pandas as pd
import io

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")  # 업로드 페이지


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "파일이 없습니다. 다시 업로드 해주세요.", 400

    file = request.files["file"]
    if file.filename == "":
        return "파일 이름이 없습니다. 다시 업로드 해주세요.", 400

    if file:
        # 데이터를 메모리에서 바로 읽어 처리
        try:
            df = pd.read_csv(io.StringIO(file.stream.read().decode("utf-8")))
        except Exception as e:
            return f"파일을 읽는 중 오류가 발생했습니다: {e}", 400

        # 데이터 처리
        result = process_file(df)

        # 결과를 HTML 테이블로 보여줌
        return render_template("result.html", rows=result.values)


def process_file(df):
    # 모든 기술 스택을 소문자로 변환 후 빈도수 계산
    tech_stacks = []
    for row in df.iloc[:, 0]:  # 첫 번째 열 사용
        tech_stacks.extend([item.strip().lower() for item in row.split(",")])

    result = pd.Series(tech_stacks).value_counts().reset_index()
    result.columns = ["기술 스택", "빈도수"]

    # 모든 항목에서 개행문자 제거
    result["기술 스택"] = result["기술 스택"].str.replace("\n", " ", regex=False)
    return result


if __name__ == "__main__":
    app.run(debug=True)
