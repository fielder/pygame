#include <stdint.h>
#include <string.h>

/* Note the render buffer is organized as an array of screen columns,
 * not the usual array of rows. */
static uint8_t *r_buf;
static int r_w, r_h;

void
setup (uint8_t *screen_buf, int w, int h)
{
	r_buf = screen_buf;
	r_w = w;
	r_h = h;
}

void
setPixel (int idx, uint8_t val)
{
	r_buf[idx] = val;
}

void
clear (int c)
{
	memset (r_buf, c, r_w * r_h);
}

void
drawLine (int x1, int y1, int x2, int y2, int c)
{
	int x, y;
	int dx, dy;
	int sx, sy;
	int ax, ay;
	int d;

	if (0)
	{
		if (	x1 < 0 || x1 >= r_w ||
			x2 < 0 || x2 >= r_w ||
			y1 < 0 || y1 >= r_h ||
			y2 < 0 || y2 >= r_h )
		{
			return;
		}
	}

	dx = x2 - x1;
	ax = 2 * (dx < 0 ? -dx : dx);
	sx = dx < 0 ? -1 : 1;

	dy = y2 - y1;
	ay = 2 * (dy < 0 ? -dy : dy);
	sy = dy < 0 ? -1 : 1;

	x = x1;
	y = y1;

	if (ax > ay)
	{
		d = ay - ax / 2;
		while (1)
		{
			r_buf[x * r_h + y] = c;
			if (x == x2)
				break;
			if (d >= 0)
			{
				y += sy;
				d -= ax;
			}
			x += sx;
			d += ay;
		}
	}
	else
	{
		d = ax - ay / 2;
		while (1)
		{
			r_buf[x * r_h + y] = c;
			if (y == y2)
				break;
			if (d >= 0)
			{
				x += sx;
				d -= ay;
			}
			y += sy;
			d += ax;
		}
	}
}
