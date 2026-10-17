import database


def test_add_task(test_db):
    """gorev ekleme basit test"""
    tid = database.add_task("Learn Pytest", test_db)
    assert tid == 1

    tasks = database.get_tasks(test_db)
    assert len(tasks) == 1
    assert tasks[0]["description"] == "Learn Pytest"
    assert tasks[0]["completed"] == 0


def test_add_multiple_tasks(test_db):
    """birden fazla gorev ekleyince hepsi gelmeli"""
    database.add_task("Task 1", test_db)
    database.add_task("Task 2", test_db)
    database.add_task("Task 3", test_db)

    tasks = database.get_tasks(test_db)
    assert len(tasks) == 3


def test_add_task_special_chars(test_db):
    """ozel karakterli gorev ekleyebilmeliyim"""
    desc = "Görev: proje %100 tamamla!"
    database.add_task(desc, test_db)
    task = database.get_tasks(test_db)[0]
    assert task["description"] == desc


def test_added_task_not_completed(test_db):
    """yeni eklenen gorev tamamlanmamis olmali"""
    database.add_task("yeni gorev", test_db)
    task = database.get_tasks(test_db)[0]
    assert task["completed"] == 0