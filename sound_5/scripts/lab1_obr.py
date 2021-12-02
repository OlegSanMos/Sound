import numpy as np
import matplotlib.pyplot as plt

def speedOfSound(temperature, h2oX, co2Max):
    #СИ
    co2Max /= 100
    temperature += 273.15
    #h2o
    xh2o = h2oX * (1 - co2Max)
    uh2o = 18.01 * xh2o
    cph2o = 1.863 * uh2o
    cvh2o = 1.403 * uh2o
    #co2
    uco2 = 44.01 * co2Max
    cpco2 = 0.838 * uco2
    cvco2 = 0.249 * uco2
    #air
    uv = 28.97 * (1 - xh2o)
    cpv =  1.0036 * uv
    cvv = 0.7166 * uv
    #gamma
    y = (cpv + cph2o + cpco2) / (cvv + cvh2o + cvco2)
    #speed
    soundSpeed = (y * 8.314 * temperature * 1000 / (uv + uh2o + uco2)) ** 0.5
    
    return soundSpeed

#assembling data
temp = 24.7
h2oX = 0.0069 #абс влажность
conc = np.linspace(0, 5, 10)
speed = speedOfSound(temp, h2oX, conc)
conc *= 100
k = np.polyfit(speed, conc, 1)
#direct measures
speed1 = 344.6
speed2 = 342.6
conc1 = np.polyval(k, speed1)
conc2 = np.polyval(k, speed2)

#building plot
fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
ax.plot(conc, speed, label='Аналитическая зависимость', linewidth=0.8)

#direct measures
ax.plot(conc1, speed1, marker = '*', label = 'Значение в воздухе: {:.1f} [м/с], {:.1f} [%]'.format(speed1, conc1), markersize=5, linewidth=0)
ax.plot(conc2, speed2, marker = '*', label = 'Значение в выдохе: {:.1f} [м/с], {:.1f} [%]'.format(speed2, conc2), markersize=5, linewidth=0)
#

ax.legend(fontsize=10)

ax.grid(which="major", linewidth=0.5)
ax.grid(which="minor", linestyle='--', linewidth=0.25)
plt.minorticks_on()

ax.axis([0 - 0.2, 5 + 0.2, speed.min() - 0.2, speed.max() + 0.2])

fig.subplots_adjust(bottom=0.15, left=0.2)

ax.set_title('Зависимость скорости звука\nот концентрации углекислого газа', loc='center', fontsize=15)
ax.set_ylabel('Скорость звука [м/с]', loc='center', fontsize=10)
ax.set_xlabel('Концентрация $CO_{2}$ [%]', loc='center', fontsize=10)

plt.show()

fig.savefig("speed-of-sound.png")

