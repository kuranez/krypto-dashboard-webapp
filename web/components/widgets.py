import panel as pn


def create_symbol_selector(options: list, value: str) -> pn.widgets.Select:
	return pn.widgets.Select(
		name='Select Cryptocurrency',
		options=options,
		value=value,
		width=200,
		margin=(5, 10)
	)


def create_period_selector(options: list, value: str) -> pn.widgets.Select:
	return pn.widgets.Select(
		name='Time Period',
		options=options,
		value=value,
		width=150,
		margin=(5, 10)
	)


def create_range_widgets() -> tuple[pn.widgets.IntRangeSlider, pn.pane.Markdown]:
	range_idx = pn.widgets.IntRangeSlider(
		name='', start=0, end=1, value=(0, 1), step=1,
		sizing_mode='stretch_width', margin=(5, 10), disabled=True,
		show_value=False
	)
	range_label = pn.pane.Markdown(
		"", sizing_mode='stretch_width', styles={'color': '#47356A', 'font-size': '20px'}, margin=(0, 5)
	)
	return range_idx, range_label

