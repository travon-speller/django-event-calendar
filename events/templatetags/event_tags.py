from django import template
from events.models import Event

register = template.Library()

@register.tag
def get_upcoming_events(parser, token):
	"""
		{% get_upcoming_events as events %}
		{% get_upcoming_events as events with num=5 days=180 %}
		5 = number of events
		60 = in the next 60 days
	"""
	bits = token.split_contents()
	if len(bits) == 3:
		# Get all the upcoming events.
		if bits[1] != 'as':
			raise template.TemplateSyntaxError("Second argument to 'get_upcoming_events' must be 'as': {% get_upcoming_events as events %}")
		return UpcomingEventsNode(bits[2])
	if len(bits) > 3:
		# Some options were specified.
		if bits[3] != 'with':
			raise template.TemplateSyntaxError("get_upcoming_events expects paramters if using 'with'")
		if len(bits) < 5:
			raise template.TemplateSyntaxError("get_upcoming_events expects paramters if using 'with'")
		kwargs = {}
		for arg in bits[4:]:
			key, value = arg.split('=')
			kwargs.update({str(key):value})
		return UpcomingEventsNode(bits[2], **kwargs)
	
class UpcomingEventsNode(template.Node):
	
	def __init__(self, varname, num=None, days=None):
		self.varname = varname
		self.num = num
		self.days = days
		
	def render(self, context):
		events = Event.on_site.upcoming(self.days)
		if self.num is None:
			context[self.varname] = events
		else:
			context[self.varname] = events[:int(self.num)]
		return u''