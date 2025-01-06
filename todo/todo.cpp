#include <iostream>
#include <fstream>
#include <vector>
#include <string>

struct Task {
    int id;
    std::string name;
    bool isCompleted;
};

std::vector<Task> tasks;

void addTask() {
    Task task;
    task.id = tasks.size() + 1;
    std::cout << "Enter task name: ";
    std::cin.ignore();
    std::getline(std::cin, task.name);
    task.isCompleted = false;
    tasks.push_back(task);
    std::cout << "Task added successfully!\n";
}

void displayTasks() {
    std::cout << "To-Do List:\n";
    for (const auto &task : tasks) {
        std::cout << task.id << ". " << task.name << " [" << (task.isCompleted ? "Completed" : "Pending") << "]\n";
    }
}

void markComplete() {
    int id;
    std::cout << "Enter task ID to mark as complete: ";
    std::cin >> id;
    if (id > 0 && id <= tasks.size()) {
        tasks[id - 1].isCompleted = true;
        std::cout << "Task marked as complete!\n";
    } else {
        std::cout << "Invalid Task ID!\n";
    }
}

void saveToFile() {
    std::ofstream file("tasks.csv");
    file << "ID,Task,Status\n";
    for (const auto &task : tasks) {
        file << task.id << "," << task.name << "," << (task.isCompleted ? "Completed" : "Pending") << "\n";
    }
    file.close();
    std::cout << "Tasks saved to tasks.csv\n";
}

int main() {
    int choice;
    do {
        std::cout << "\n1. Add Task\n2. Display Tasks\n3. Mark Task Complete\n4. Save & Exit\nEnter choice: ";
        std::cin >> choice;

        switch (choice) {
            case 1: addTask(); break;
            case 2: displayTasks(); break;
            case 3: markComplete(); break;
            case 4: saveToFile(); break;
            default: std::cout << "Invalid choice!\n";
        }
    } while (choice != 4);

    return 0;
}
