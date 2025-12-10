CARD_CSS = """
<style>
.user-card {
  background: linear-gradient(90deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  border-radius: 12px;
  padding: 14px;
  box-shadow: 0 4px 14px rgba(2,6,23,0.6);
  border: 1px solid rgba(255,255,255,0.03);
  transition: transform .08s ease-in-out;
}
.user-card:hover { transform: translateY(-4px); }
.user-avatar {
  width: 48px; height: 48px; border-radius: 10px;
  display:inline-block; text-align:center; line-height:48px; font-weight:700;
  background: linear-gradient(135deg,#3b82f6,#7c3aed); color:white;
}
.user-name { font-size: 16px; font-weight: 700; margin: 0; }
.user-meta { color: rgba(255,255,255,0.7); margin: 0; font-size: 13px; }
.view-button { margin-top:8px; }
</style>
"""


UPDATE_CARD_STYLE = """
<style>
.exp-card {
  border-radius: 12px;
  padding: 14px;
  margin-bottom: 12px;
  background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  border: 1px solid rgba(255,255,255,0.03);
  box-shadow: 0 6px 20px rgba(2,6,23,0.6);
}
.exp-row { display:flex; gap:16px; align-items:center; justify-content:space-between; }
.exp-left { display:flex; gap:14px; align-items:center; }
.avatar {
  width:44px; height:44px; border-radius:10px; font-weight:700;
  display:flex; align-items:center; justify-content:center;
  background: linear-gradient(135deg,#ef4444,#f97316); color:white;
}
.exp-meta { color: rgba(255,255,255,0.75); font-size:13px; }
.exp-amount { font-weight:800; font-size:18px; color: #fff; text-align:right; }
.small-muted { color: rgba(255,255,255,0.6); font-size:12px; }
.btn-row { display:flex; gap:8px; }
.card-actions button {
  background: transparent; border: 1px solid rgba(255,255,255,0.06); color: #fff;
  padding: 6px 10px; border-radius:8px; cursor:pointer;
}
.card-actions .edit { background: linear-gradient(90deg,#60a5fa,#7c3aed); border:none; }
.form-row { margin-top:10px; }
</style>
"""
