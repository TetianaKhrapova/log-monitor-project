from monitor iport load_config

def test_config_load(tmp_path):
    cfg = {"log_path": "x", "keywords": ["ERR"]}
    p = tmp_path / "cffg.yaml"
    p.write_text("log_path: x/nkeywords:\n - ERR\n")
    c = load_config(str(p))
    assert c['log_path'] == "x"
    assert "ERR" in c['keywords']
