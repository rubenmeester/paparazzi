/*
 * Copyright (C) nilay
 *
 * This file is part of paparazzi
 *
 * paparazzi is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2, or (at your option)
 * any later version.
 *
 * paparazzi is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with paparazzi; see the file COPYING.  If not, see
 * <http://www.gnu.org/licenses/>.
 */
/**
 * @file "modules/percevite_wifi/percevite_wifi.h"
 * @author nilay
 * wifi ssid broadcast
 */

#ifndef PERCEVITE_WIFI_H
#define PERCEVITE_WIFI_H

#include "mcu_periph/uart.h"

#define ESP_UART_PORT uart2


extern void uart_esp_init(void);
extern void uart_esp_loop(void);

#endif

