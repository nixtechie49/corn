__author__ = 'rock'

# from com.jd.flow import AdGroupInfo_pb2, MediaInfo_pb2
#
#
# class MediaId():
# def do(self, value=None):
#         m = MediaInfo_pb2.MediaInfo()
#         m.ParseFromString(value)
#         value = r'media_id:%d , media_name:%s , media_type:%s , url:%s , billing_type:%d , width:%d , height:%d , content:%s , spread_type:%d , publish_type:%d , put_type:%d , ad_id:%d , yn:%d' % (
#             m.media_id, m.media_name, m.media_type, m.url, m.billing_type, m.width, m.height, m.content, m.spread_type,
#             m.publish_type, m.put_type, m.ad_id, m.yn)
#         return value
#
#
# class AdGroupId():
#     def do(self, value=None):
#         a = AdGroupInfo_pb2.AdGroupInfo()
#         a.ParseFromString(value)
#         ai = ''
#         for adinfo in a.adinfo:
#             ai += ('adinfo[adId:%d , adName:%s , width:%d , height:%d , content:%s]' % (
#                 adinfo.adId, adinfo.adName, adinfo.width, adinfo.height, adinfo.content))
#         value = r'group_id:%d , campaign_id:%d , name:%s , position:%s , group_direction:%s , created_time:%s , budget:%d , price:%d , billing_type:%d , put_type:%d , %s' % (
#             a.group_id, a.campaign_id, a.name, a.position, a.group_direction, a.created_time, a.budget, a.price,
#             a.billing_type, a.put_type, ai)
#         return value


MAP = {}
# MAP = {ur'(media:id:\d)': MediaId(), ur'(adGroup:id:\d)': AdGroupId()}
