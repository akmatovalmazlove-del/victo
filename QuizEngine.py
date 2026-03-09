import json
import random
from typing import Optional, Dict, Any

class QuizEngine:
    def __init__(self, filename: str = "questions.json"):
        """
        Инициализация движка викторины
        Загружает вопросы из JSON-файла
        """
        self.current_level: int = 1
        self.questions: Dict[int, list] = {}      # уровень → список вопросов
        self.current_question: Optional[Dict[str, Any]] = None
        
        self._load_questions(filename)

    def _load_questions(self, filename: str) -> None:
        """Загружает и группирует вопросы по уровням"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Ожидаем структуру: список словарей, каждый с полем "level"
            for q in data:
                level = q.get("level")
                if not isinstance(level, int) or level < 1:
                    continue
                    
                if level not in self.questions:
                    self.questions[level] = []
                    
                self.questions[level].append(q)
                
            if not self.questions:
                raise ValueError("В файле нет корректных вопросов с указанным level")
                
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {filename} не найден")
        except json.JSONDecodeError:
            raise ValueError(f"Файл {filename} содержит некорректный JSON")
        except Exception as e:
            raise Exception(f"Ошибка при загрузке вопросов: {e}")

    def get_next_question(self) -> Optional[Dict[str, Any]]:
        """
        Возвращает случайный вопрос текущего уровня
        Возвращает None, если вопросов на текущем уровне больше нет
        """
        if self.current_level not in self.questions or not self.questions[self.current_level]:
            return None
            
        self.current_question = random.choice(self.questions[self.current_level])
        return self.current_question

    def check_answer(self, user_answer: str) -> bool:
        """
        Проверяет ответ пользователя
        Возвращает True если правильно, False если нет
        При правильном ответе повышает уровень
        """
        if self.current_question is None:
            return False
            
        correct = self.current_question.get("correct_answer", "").strip().lower()
        user = str(user_answer).strip().lower()
        
        is_correct = (user == correct)
        
        if is_correct:
            self.current_level += 1
            
        # Можно раскомментировать, если нужно удалять использованный вопрос
        # self.questions[self.current_level - 1].remove(self.current_question)
        
        self.current_question = None  # сбрасываем текущий вопрос после ответа
        
        return is_correct

    def get_current_level(self) -> int:
        """Возвращает текущий уровень"""
        return self.current_level


# Пример использования:
if __name__ == "__main__":
    # Пример структуры questions.json:
    """
    [
        {"level": 1, "question": "Столица Франции?", "correct_answer": "Париж"},
        {"level": 1, "question": "2 + 2 = ?", "correct_answer": "4"},
        {"level": 2, "question": "Самая длинная река в мире?", "correct_answer": "Нил"},
        {"level": 3, "question": "Скорость света в вакууме (км/с)?", "correct_answer": "300000"}
    ]
    """
    
    try:
        engine = QuizEngine("questions.json")
        
        while True:
            q = engine.get_next_question()
            if q is None:
                print(f"Вопросы уровня {engine.get_current_level()} закончились!")
                break
                
            print(f"\nУровень {engine.get_current_level()}:")
            print(q["question"])
            answer = input("Ваш ответ: ")
            
            if engine.check_answer(answer):
                print("Правильно! Переходим на следующий уровень.")
            else:
                print(f"Неправильно. Правильный ответ: {q.get('correct_answer')}")
                print("Игра окончена.")
                break
                
    except Exception as e:
        print(f"Ошибка: {e}")