nЛабораторна робота №7
Computer Vision та багатопотоковість у C++
дедлайн 23 травня
Мета роботи
Навчитися поєднувати класичне програмування на C++ із сучасним CV/ML. Освоїти роботу з cv::dnn (Deep Neural Networks) для детекції об'єктів. Зрозуміти проблему блокування інтерфейсу важкими обчисленнями та вирішити її за допомогою std::thread та std::mutex, або std::condition_variable.
Робота виконується на базі вашого коду з попередньої лабораторної роботи. В preinstall.sh треба додати завантаження нейронки.
Завдання: Рівень 1 (Базовий, 50% оцінки)
Ваша програма повинна мати новий режим обробки (вмикається клавішею, наприклад F - Face), який виконує детекцію облич на відео. Ми використаємо сучасний підхід - детектор на базі ResNet-10 (йде в прикладах OpenCV). Вам знадобляться два файли (додайте команди їх завантаження з wget у ваш preinstall.sh):
Архітектура: deploy.prototxt (https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt)
Ваги: res10_300x300_ssd_iter_140000.caffemodel (https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel)


