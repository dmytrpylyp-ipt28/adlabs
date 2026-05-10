"""
ІНСТРУКЦІЯ КОРИСТУВАЧА:
1. Використовуйте слайдери Amplitude/Frequency для зміни сигналу.
2. Слайдери Noise Mean/Cov змінюють параметри випадкових завад.
3. Cutoff Frequency регулює ступінь очищення сигналу фільтром.
4. Кнопка Reset повертає початкові налаштування.
5. Чекбокс Show Noise приховує або показує зашумлений графік.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy.signal import butter, lfilter

def butter_lowpass_filter(data, cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return lfilter(b, a, data)

t = np.linspace(0, 10, 1000)
fs = 100
init_amp = 1.0
init_freq = 0.3
init_phase = 0.0
init_noise_mean = 0.0
init_noise_cov = 0.1
init_cutoff = 5.0

current_noise = np.random.normal(init_noise_mean, np.sqrt(init_noise_cov), len(t))

fig, ax = plt.subplots(figsize=(10, 8))
plt.subplots_adjust(bottom=0.4) # Місце для слайдерів

line_noise, = ax.plot(t, np.zeros(len(t)), color='orange', alpha=0.6, label='Зашумлена')
line_clean, = ax.plot(t, np.zeros(len(t)), 'b--', label='Чиста')
line_filtered, = ax.plot(t, np.zeros(len(t)), color='purple', linewidth=2, label='Відфільтрована')

ax.legend(loc='upper right')
ax.set_ylim(-3, 3)

ax_amp = plt.axes([0.25, 0.30, 0.50, 0.03])
ax_freq = plt.axes([0.25, 0.25, 0.50, 0.03])
ax_phase = plt.axes([0.25, 0.20, 0.50, 0.03])
ax_n_mean = plt.axes([0.25, 0.15, 0.50, 0.03])
ax_n_cov = plt.axes([0.25, 0.10, 0.50, 0.03])
ax_cutoff = plt.axes([0.25, 0.05, 0.50, 0.03])

s_amp = Slider(ax_amp, 'Amplitude', 0.1, 2.0, valinit=init_amp)
s_freq = Slider(ax_freq, 'Frequency', 0.01, 1.0, valinit=init_freq)
s_phase = Slider(ax_phase, 'Phase', 0.0, 2*np.pi, valinit=init_phase)
s_n_mean = Slider(ax_n_mean, 'Noise Mean', -1.0, 1.0, valinit=init_noise_mean)
s_n_cov = Slider(ax_n_cov, 'Noise Cov', 0.0, 1.0, valinit=init_noise_cov)
s_cutoff = Slider(ax_cutoff, 'Cutoff Freq', 0.1, 10.0, valinit=init_cutoff)

rax = plt.axes([0.8, 0.02, 0.15, 0.04])
check = CheckButtons(rax, ['Show Noise'], [True])
resetax = plt.axes([0.1, 0.02, 0.1, 0.04])
button = Button(resetax, 'Reset', color='lightblue', hovercolor='0.975')

def update(val):
    global current_noise
    
    amp = s_amp.val
    freq = s_freq.val
    phase = s_phase.val
    n_mean = s_n_mean.val
    n_cov = s_n_cov.val
    cutoff = s_cutoff.val
    
    y_clean = amp * np.sin(2 * np.pi * freq * t + phase)
    
    current_noise = np.random.normal(n_mean, np.sqrt(n_cov), len(t))
    
    y_noisy = y_clean + current_noise
    y_filtered = butter_lowpass_filter(y_noisy, cutoff, fs)
    
    line_clean.set_ydata(y_clean)
    line_filtered.set_ydata(y_filtered)
    
    if check.get_status()[0]:
        line_noise.set_ydata(y_noisy)
    else:
        line_noise.set_ydata(y_clean)
        
    fig.canvas.draw_idle()

def reset(event):
    s_amp.reset()
    s_freq.reset()
    s_phase.reset()
    s_n_mean.reset()
    s_n_cov.reset()
    s_cutoff.reset()

s_amp.on_changed(update)
s_freq.on_changed(update)
s_phase.on_changed(update)
s_n_mean.on_changed(update)
s_n_cov.on_changed(update)
s_cutoff.on_changed(update)
button.on_clicked(reset)
check.on_clicked(update)

update(None)
plt.show()