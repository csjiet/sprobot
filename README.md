
Slack API
- Create a Slack API from [api.slack.com](api.slack.com)

Twitter API
- Create a developer portal from [developer.twitter.com](developer.twitter.com)
- Tweet lookups (Documentation) [https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/quick-start](https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/quick-start)


# [Github](https://github.com/JustAnotherArchivist/snscrape/blob/master/snscrape/modules/twitter.py)
Snscrape Tweet fields:
- url: str
- date: datetime.datetime
- rawContent: str
- renderedContent: str
- id: int
- user: typing.Union['User', 'UserRef']
- replyCount: int
- retweetCount: int
- likeCount: int
- quoteCount: int
- conversationId: int
- lang: str
- source: typing.Optional[str] = None
- sourceUrl: typing.Optional[str] = None
- sourceLabel: typing.Optional[str] = None
- links: typing.Optional[typing.List['TextLink']] = None
- media: typing.Optional[typing.List['Medium']] = None
- retweetedTweet: typing.Optional['Tweet'] = None
- quotedTweet: typing.Optional['Tweet'] = None
- inReplyToTweetId: typing.Optional[int] = None
- inReplyToUser: typing.Optional['User'] = None
- mentionedUsers: typing.Optional[typing.List['User']] = None
- coordinates: typing.Optional['Coordinates'] = None
- place: typing.Optional['Place'] = None
- hashtags: typing.Optional[typing.List[str]] = None
- cashtags: typing.Optional[typing.List[str]] = None
- card: typing.Optional['Card'] = None
- viewCount: typing.Optional[int] = None
- vibe: typing.Optional['Vibe'] = None
- bookmarkCount: typing.Optional[int] = None
- pinned: typing.Optional[bool] = None
- editState: typing.Optional['EditState'] = None
- conversationControlPolicy: typing.Optional['ConversationControlPolicy'] = None
- username = snscrape.base._DeprecatedProperty('username', lambda self: getattr(self.user, 'username', None), 'user.username')
- outlinks = snscrape.base._DeprecatedProperty('outlinks', lambda self: [x.url for x in self.links] if self.links else [], 'links (url attribute)')
- outlinksss = snscrape.base._DeprecatedProperty('outlinksss', lambda self: ' '.join(x.url for x in self.links) if self.links else '', 'links (url attribute)')
- tcooutlinks = snscrape.base._DeprecatedProperty('tcooutlinks', lambda self: [x.tcourl for x in self.links] if self.links else [], 'links (tcourl attribute)')
- tcooutlinksss = snscrape.base._DeprecatedProperty('tcooutlinksss', lambda self: ' '.join(x.tcourl for x in self.links) if self.links else '', 'links (tcourl attribute)')
- content = snscrape.base._DeprecatedProperty('content', lambda self: self.rawContent, 'rawContent')