        import shutil
        import os
        from datetime import datetime

        def backup_database(db_path, backup_dir):
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = os.path.join(backup_dir, f'accounts_backup_{timestamp}.db')
            shutil.copyfile(db_path, backup_file)
            return backup_file

        def restore_database(backup_file, db_path):
            shutil.copyfile(backup_file, db_path)