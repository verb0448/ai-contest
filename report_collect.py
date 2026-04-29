import streamlit as st
from supabase import create_client, Client
from datetime import datetime
import re

st.set_page_config(
    page_title="AI 경진대회 출품",
    page_icon="\U0001f916",
    layout="centered",
    initial_sidebar_state="collapsed"
)

LOGO_B64 = "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"

@st.cache_resource
def get_supabase() -> Client:
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

supabase = get_supabase()

st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css');

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none !important; }

/* ── 배경 ── */
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 55% at 20% 30%, rgba(0,180,200,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 60% 45% at 80% 70%, rgba(0,120,180,0.22) 0%, transparent 60%),
        radial-gradient(ellipse 50% 35% at 55% 10%, rgba(0,200,220,0.12) 0%, transparent 55%),
        linear-gradient(160deg, #020a18 0%, #030d20 40%, #021018 70%, #030e22 100%);
    background-attachment: fixed;
    min-height: 100vh;
}
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed; inset: 0;
    background-image:
        radial-gradient(1px 1px at 15% 20%, rgba(255,255,255,0.55) 0%, transparent 100%),
        radial-gradient(1px 1px at 55% 15%, rgba(255,255,255,0.40) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 80% 8%,  rgba(255,255,255,0.50) 0%, transparent 100%),
        radial-gradient(1px 1px at 8%  55%, rgba(255,255,255,0.30) 0%, transparent 100%),
        radial-gradient(1px 1px at 92% 45%, rgba(255,255,255,0.35) 0%, transparent 100%),
        radial-gradient(2px 2px at 48% 42%, rgba(0,200,255,0.35) 0%, transparent 100%);
    pointer-events: none; z-index: 0;
}

/* ── 글래스 카드 ── */
[data-testid="stAppViewBlockContainer"],
.block-container {
    max-width: 480px !important;
    margin-top: 4rem !important;
    padding: 2.5rem 2.2rem 2rem !important;
    background: rgba(255,255,255,0.04) !important;
    backdrop-filter: blur(12px) saturate(150%) !important;
    -webkit-backdrop-filter: blur(12px) saturate(150%) !important;
    border: 1px solid rgba(0,200,230,0.18) !important;
    border-radius: 24px !important;
    box-shadow: 0 8px 40px rgba(0,0,0,0.50), inset 0 1px 0 rgba(0,220,255,0.12) !important;
}

/* ── 라벨 ── */
.stTextInput label p,
.stFileUploader label p,
[data-testid="stWidgetLabel"] p {
    color: rgba(160,230,255,0.90) !important;
    font-family: 'Pretendard', sans-serif !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    letter-spacing: 0.3px !important;
}

/* ── 텍스트 인풋 ── */
[data-testid="stTextInput"] input,
div[data-baseweb="input"] input {
    background: rgba(0,200,255,0.06) !important;
    border: 1px solid rgba(0,200,230,0.25) !important;
    border-radius: 50px !important;
    color: #ffffff !important;
    font-family: 'Pretendard', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    padding: 12px 18px !important;
    caret-color: #00d4ff !important;
}
[data-testid="stTextInput"] input:focus {
    background: rgba(0,200,255,0.10) !important;
    border-color: rgba(0,210,255,0.70) !important;
    box-shadow: 0 0 0 3px rgba(0,180,230,0.18) !important;
}
[data-testid="stTextInput"] input::placeholder {
    color: rgba(160,220,255,0.35) !important;
    font-weight: 500 !important;
}
div[data-baseweb="input"],
div[data-baseweb="base-input"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* ── 파일 업로더: 컨테이너만 스타일 (버튼 CSS 제거 → 이중 텍스트 방지) ── */
[data-testid="stFileUploader"] section {
    background: rgba(0,200,255,0.06) !important;
    border: 1px solid rgba(0,200,230,0.25) !important;
    border-radius: 16px !important;
}
[data-testid="stFileUploader"] section small,
[data-testid="stFileUploader"] section span:not([data-testid]) {
    color: rgba(160,230,255,0.70) !important;
    font-family: 'Pretendard', sans-serif !important;
}

/* ── 제출 버튼 (use_container_width로 너비 해결, CSS는 색상만) ── */
[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #00b4d8, #0077b6) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 50px !important;
    font-family: 'Pretendard', sans-serif !important;
    font-size: 15px !important;
    font-weight: 800 !important;
    letter-spacing: 0.5px !important;
    box-shadow: 0 4px 20px rgba(0,150,200,0.40) !important;
}
[data-testid="stFormSubmitButton"] > button:hover {
    background: linear-gradient(135deg, #00c8f0, #0088cc) !important;
    box-shadow: 0 6px 28px rgba(0,180,230,0.55) !important;
    transform: translateY(-1px) !important;
}
[data-testid="stFormSubmitButton"] > button p {
    color: #ffffff !important;
    font-size: 15px !important;
    font-weight: 800 !important;
}

/* ── 알림 ── */
[data-testid="stAlert"] {
    background: rgba(0,150,200,0.12) !important;
    border: 1px solid rgba(0,200,230,0.25) !important;
    border-radius: 14px !important;
}
[data-testid="stAlert"] p { color: #ffffff !important; }

.hint-text {
    font-size: 11px !important;
    color: rgba(255,210,100,0.85) !important;
    margin-top: -8px !important;
    margin-bottom: 8px !important;
    padding-left: 10px !important;
    font-family: 'Pretendard', sans-serif !important;
}
.custom-divider {
    width: 48px; height: 2px;
    background: linear-gradient(90deg, transparent, rgba(0,200,255,.7), transparent);
    margin: 6px auto 24px; border-radius: 2px;
}
</style>
""", unsafe_allow_html=True)

# ── 로고 + 타이틀 ──────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center; margin-bottom:4px;">
    <img src="data:image/png;base64,{LOGO_B64}"
         style="max-width:210px; max-height:52px; object-fit:contain;
                filter:drop-shadow(0 0 10px rgba(0,200,255,.5));">
</div>
<h2 style="text-align:center; color:#fff; font-family:'Pretendard',sans-serif;
           font-weight:800; font-size:24px; letter-spacing:-0.3px; margin:0 0 2px;
           text-shadow:0 0 20px rgba(0,180,255,.9), 0 0 40px rgba(0,120,200,.5);">
    AI 경진대회 출품
</h2>
<div class="custom-divider"></div>
""", unsafe_allow_html=True)

# ── 폼 ─────────────────────────────────────────────────────────
with st.form("submission_form", clear_on_submit=True):
    org = st.text_input("조직", placeholder="소속 조직을 입력하세요")
    st.markdown(
        '<p class="hint-text">* 영업부문의 경우 총괄단위까지 기재</p>',
        unsafe_allow_html=True
    )
    name = st.text_input("성명", placeholder="성명을 입력하세요")
    uploaded_file = st.file_uploader(
        "자료 제출",
        type=["doc","docx","pdf","ppt","pptx","xls","xlsx","hwp","hwpx","zip","png","jpg"],
        help="Word, PDF, HWP, PPT 등 제출 자료를 첨부해 주세요."
    )
    # use_container_width=True → 버튼 너비 100% (CSS 불필요)
    submitted = st.form_submit_button("제출", use_container_width=True)

# ── 제출 처리 ──────────────────────────────────────────────────
if submitted:
    if not org.strip():
        st.error("조직을 입력해 주세요.")
    elif not name.strip():
        st.error("성명을 입력해 주세요.")
    elif uploaded_file is None:
        st.error("제출할 파일을 첨부해 주세요.")
    else:
        with st.spinner("제출 중..."):
            try:
                # 파일 확장자 추출
                ext = uploaded_file.name.rsplit('.', 1)[-1] if '.' in uploaded_file.name else 'bin'
                
                # Storage 키: 타임스탬프만 사용 (한글/특수문자 제거)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                org_safe  = re.sub(r'[^A-Za-z0-9]', '', org.strip())   # 영문/숫자만
                name_safe = re.sub(r'[^A-Za-z0-9]', '', name.strip())  # 영문/숫자만
                file_safe = re.sub(r'[^A-Za-z0-9_\-\.]', '', uploaded_file.name)  # 원본파일명 특수문자 제거
                safe_name = f"{timestamp}_{org_safe}_{name_safe}_{file_safe}"
                
                file_bytes = uploaded_file.read()

                supabase.storage \
                    .from_("ai-contest-files") \
                    .upload(
                        path=safe_name,
                        file=file_bytes,
                        file_options={"content-type": uploaded_file.type or "application/octet-stream"}
                    )

                SUPABASE_URL = st.secrets["SUPABASE_URL"]
                file_url = f"{SUPABASE_URL}/storage/v1/object/public/ai-contest-files/{safe_name}"

                supabase.table("submissions").insert({
                    "org"      : org.strip(),
                    "name"     : name.strip(),
                    "file_name": uploaded_file.name,  # 원본 파일명은 DB에 저장
                    "file_url" : file_url,
                }).execute()

                st.success("✅  제출이 완료되었습니다.  참여해 주셔서 감사합니다!")

            except Exception as e:
                st.error(f"오류가 발생했습니다. 잠시 후 다시 시도해 주세요.\n\n{str(e)}")