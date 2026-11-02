# GROUP COLS
FORCE_COLS = ('Fx_t', 'Fx_l', 'Fx_r', 'Fy_t', 'Fy_l', 'Fy_r', 'Fz_t', 'Fz_l', 'Fz_r')

COMP_FORCE_COLS_MAP = {f:f"comp_{f}" for f in FORCE_COLS}

AMTI_TO_FORCE_COLS_MAP = {"Fxl12":"Fx_l",
                          "Fxr12":"Fx_r",
                          "Fyl14":"Fy_l",
                          "Fyr14":"Fy_r",
                          "Fzl1":"Fz_l",
                          "Fzr1":"Fz_r"}