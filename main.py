from mamba_login_gui import LoginGUI
from mamba_account_database import MambaAccountDB
from mamba_password_vault_database import MambaPasswordVaultDB

if __name__ == "__main__":
    db = MambaAccountDB()
    pv_db = MambaPasswordVaultDB()
    db.create_mamba_account_table()
    pv_db.create_mamba_password_vault_table()
    login = LoginGUI(db)
