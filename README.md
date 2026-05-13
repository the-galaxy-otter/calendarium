# Paradigm and data model
## Formatting
Timeline represents infinite scale, positive and negative, represented by integer value meaning secons since 0.
All moments and spans are objectively defined on the timeline with unambigous position. This project does not care about causal structure, only cares about temporal events. Timelines can be joined together and mapped to each-other. Manager has a default 1:1 timeline in it. Timelines are defined with offset and shrinking/extending parameter relative to default timeline. Non-default timelines can also have skips, as holes on the scale relative to default timeline.

Calendars are definitions of repeatable sets of periods, that can be projected onto the timeline. It allows back and forward conversion to a timeline monent/span, which can be mediated through default timeline and reconverted back. It would allow conversion between differen calndars serving connected but non-parallel timelines.
## Classes
### Timeline
Represents elements of data model used for timeline modeling and referencing points and/or spans in time.
When moment refers to integer value, it means the second it happens in. So moments need additional parameter to specify a point within the second, float valuebetween 0 and 1 Must check if value reaches out of this range. This parameter is mostly like z-index for sorting momentswithin the same second.
#### TimelineUnits
Enum, containing values for clasical units of measurement for time. It is used to define unit sets to create more readable representations of time.
#### TimelineManager
Factory class and manager to register timelines, allows processing timelines together. Manager object contains several timelines, one of which must be default one, and manages relation between tham, allowing to convert timeline moments/spans between timelines.
#### TimelineObject
Object representing timeline itself, it's fundamental properties and relations to a default timeline.
#### TimelineMoment
Represents exact point on a timeline.
#### TimelineSpan
Represents a span of time on a timeline.Spancanbe finite, or have no start/end. 
### Calendars
Classes representing calendars.
