import random
import re

# ==========================================
# 1. TU KHOA CAM XUC
# ==========================================


EMOTION_KEYWORDS = {
    "Vui vẻ": [
        "vui", "vui vẻ", "hạnh phúc", "sung sướng",
        "phấn khởi", "hân hoan", "hứng khởi",
        "hưng phấn", "thích thú", "yêu đời",
        "lạc quan", "mãn nguyện", "hài lòng",
        "thoải mái", "dễ chịu", "tuyệt vời",
        "rạng rỡ", "hớn hở", "vui sướng",
        "thỏa mãn", "tự hào", "bình yên",
        "an nhiên", "nhẹ nhõm", "thư thái",
        "ấm áp", "may mắn", "cười", "mỉm cười",
        "vui mừng", "reo vui", "phấn khích",
        "háo hức", "hào hứng", "tích cực",
        "tràn đầy năng lượng", "tâm trạng tốt",
        "cảm thấy được yêu thương", "có động lực"
    ],

    "Buồn bã": [
        "buồn", "buồn bã", "đau buồn", "cô đơn",
        "cô độc", "tủi thân", "thất vọng",
        "hụt hẫng", "chán nản", "bi quan",
        "tuyệt vọng", "u sầu", "ủ rũ", "não nề",
        "trống rỗng", "lạc lõng", "tổn thương",
        "đau lòng", "xót xa", "tiếc nuối",
        "buồn tủi", "suy sụp", "mệt mỏi",
        "rầu rĩ", "sầu muộn", "mất mát",
        "nhớ nhung", "khóc", "rơi nước mắt",
        "im lặng", "thu mình", "thở dài",
        "không còn động lực", "chỉ muốn khóc",
        "không ai hiểu mình", "bị bỏ rơi",
        "không còn hứng thú", "chẳng muốn làm gì"
    ],

    "Căng thẳng": [
        "căng thẳng", "áp lực", "quá tải",
        "kiệt sức", "căng cứng", "mệt mỏi",
        "bế tắc", "ngột ngạt", "choáng ngợp",
        "bí bách", "nặng nề", "rối ren",
        "bất ổn", "mệt nhoài", "đuối sức",
        "quá sức", "chật vật", "lao lực",
        "kiệt quệ", "gồng mình", "bức bối",
        "mất cân bằng", "căng như dây đàn",
        "áp lực học tập", "áp lực thi cử",
        "áp lực điểm số", "quá nhiều bài tập",
        "không kịp hoàn thành", "cảm thấy quá tải",
        "không có thời gian nghỉ ngơi",
        "mọi thứ dồn lên cùng lúc",
        "không thể chịu thêm nữa",
        "đầu óc căng thẳng", "cảm thấy kiệt sức",
        "áp lực từ gia đình", "không thể cân bằng",
        "công việc quá nhiều", "không có thời gian cho bản thân"
    ],

    "Lo lắng": [
        "lo lắng", "lo âu", "bất an", "hồi hộp",
        "thấp thỏm", "bồn chồn", "hoang mang",
        "sợ hãi", "lo sợ", "e ngại", "bất định","sợ"
        "nghi ngờ", "ám ảnh", "run rẩy",
        "sợ sệt", "nôn nóng", "sốt ruột",
        "phấp phỏng", "hoảng hốt", "hoảng sợ",
        "thiếu tự tin", "bối rối",
        "không biết chuyện gì sẽ xảy ra",
        "lo lắng về tương lai", "sợ thất bại",
        "sợ không đạt kết quả tốt",
        "không biết phải làm thế nào",
        "suy nghĩ tiêu cực", "nghĩ quá nhiều",
        "không thể ngừng lo lắng",
        "sợ làm người khác thất vọng",
        "lo lắng về kỳ thi", "sợ bị đánh giá",
        "không cảm thấy an toàn",
        "luôn có cảm giác bất an",
        "không thể bình tĩnh",
        "sợ những điều chưa xảy ra"
    ],

    "Tức giận": [
        "tức giận", "giận dữ", "phẫn nộ",
        "cáu kỉnh", "bực bội", "khó chịu",
        "nóng giận", "nổi nóng", "bất mãn",
        "ức chế", "căm tức", "oán giận",
        "thù ghét", "hậm hực", "hằn học",
        "bực tức", "phẫn uất", "bực mình",
        "tức tối", "cay cú", "bức xúc",
        "bất bình", "hung hăng", "nóng nảy",
        "mất bình tĩnh", "điên tiết",
        "không thể chịu đựng được",
        "không công bằng", "bị xúc phạm",
        "không ai chịu lắng nghe",
        "bị đối xử bất công", "không kiểm soát được cơn giận",
        "cảm thấy bị coi thường", "muốn hét",
        "muốn tranh cãi", "phản ứng gay gắt"
    ]
}






# ==========================================
# 2. GOI Y CHAM SOC
# ==========================================

# Mỗi cảm xúc có nhiều gợi ý; app chọn ngẫu nhiên một câu cho mỗi lần phân tích.
EMOTION_SUGGESTIONS = {
    "Vui vẻ": [
        "Hãy duy trì những hoạt động tích cực và chia sẻ niềm vui với mọi người.",
        "Bạn đang có tâm trạng tốt, hãy ghi lại điều khiến bạn vui để nhớ lại những lúc cần động lực.",
        "Thử viết ra ba điều biết ơn trong ngày hôm nay, niềm vui sẽ ở lại lâu hơn.",
        "Chia sẻ niềm vui với một người bạn tin tưởng, niềm vui được nhân đôi khi có người cùng đón nhận.",
        "Hãy tận dụng năng lượng này để làm một việc bạn vẫn hay trì hoãn.",
        "Dành một lời khen hoặc lời cảm ơn cho ai đó hôm nay, bạn sẽ thấy tâm trạng tốt hơn nữa.",
        "Đừng quên nghỉ ngơi dù đang vui, giấc ngủ đủ giúp bạn giữ được tâm trạng tích cực.",
        "Hãy dừng lại một chút và tận hưởng khoảnh khắc này, không cần vội nghĩ đến việc tiếp theo.",
        "Bạn có thể tặng bản thân một phần thưởng nhỏ vì đã cố gắng thời gian qua.",
        "Thử giúp đỡ một bạn đang gặp khó khăn, giúp người khác cũng làm niềm vui của bạn lan xa hơn.",
        "Hãy lưu lại một bức ảnh hoặc vài dòng nhật ký về ngày hôm nay để đọc lại sau này.",
        "Dùng tâm trạng tốt này để lên kế hoạch cho một mục tiêu nhỏ trong tuần tới.",
        "Hãy cùng bạn bè làm điều gì đó vui như đi dạo, chơi thể thao hoặc nghe nhạc.",
        "Niềm vui rất đáng quý, hãy cho phép bản thân vui trọn vẹn mà không cần tự trách hay lo xa.",
        "Bạn có thể thử bài thở hộp 4-4-4-4 trong Phòng luyện tập để giữ sự tập trung và tâm trạng ổn định.",
        "Hãy uống đủ nước và ăn uống đều đặn để cơ thể cũng vui cùng bạn.",
        "Chia sẻ điều tốt đẹp bạn vừa trải qua với gia đình, họ sẽ rất vui khi biết.",
        "Hãy nhớ lại cảm giác này như một nguồn lực khi gặp ngày khó khăn.",
        "Thử học thêm một điều mới nhỏ xíu hôm nay, tâm trạng tốt giúp bạn tiếp thu dễ hơn.",
        "Bạn xứng đáng với niềm vui này, hãy ghi nhận những nỗ lực đã đưa bạn đến đây.",
        "Hãy viết một lời nhắn tích cực cho bạn của ngày mai và cất đi để đọc khi cần.",
        "Đi bộ ngoài trời một lúc để cảm nhận trọn vẹn tâm trạng tốt của mình.",
        "Hãy cùng người thân dọn dẹp góc học tập, không gian gọn gàng giúp giữ tâm trạng nhẹ nhàng.",
        "Bạn có thể tập một thói quen nhỏ như đọc 10 phút mỗi ngày, khi vui thì dễ bắt đầu hơn.",
        "Đừng so sánh niềm vui của mình với người khác, mỗi người có nhịp riêng.",
        "Hãy kể lại câu chuyện vui hôm nay cho ai đó, việc kể lại giúp ký ức rõ nét hơn.",
        "Nghe một bài nhạc bạn yêu thích và để cơ thể thư giãn theo giai điệu.",
        "Hãy tập trung vào hiện tại, tận hưởng từng việc nhỏ như bữa ăn hay cuộc trò chuyện.",
        "Nếu có thể, hãy làm một việc tốt nhỏ cho môi trường xung quanh như dọn lớp hay tưới cây.",
        "Hãy ghi nhớ những người đã ở bên bạn và gửi họ một lời cảm ơn chân thành.",
        "Cân bằng giữa vui chơi và học tập sẽ giúp niềm vui bền vững hơn.",
        "Hãy tiếp tục chăm sóc bản thân bằng giấc ngủ, vận động và những mối quan hệ tốt đẹp.",
    ],

    "Buồn bã": [
        "Bạn có thể trò chuyện với người mình tin tưởng và dành thời gian chăm sóc bản thân.",
        "Cảm thấy buồn là điều bình thường, bạn không cần ép mình phải vui ngay lập tức.",
        "Hãy thử viết ra những điều đang nặng trong lòng, viết ra giúp đầu óc nhẹ hơn.",
        "Nếu có thể, hãy kể với một người bạn, người thân hoặc thầy cô mà bạn tin tưởng.",
        "Hãy cho phép bản thân khóc nếu cần, nước mắt đôi khi giúp bạn nhẹ lòng hơn.",
        "Bạn có thể thử bài Quét cơ thể trong Phòng luyện tập để đưa sự chú ý về hiện tại một cách nhẹ nhàng.",
        "Ra ngoài đi bộ 10 đến 15 phút, ánh sáng và không khí có thể giúp tâm trạng khá hơn.",
        "Hãy làm một việc nhỏ dễ dàng như tắm nước ấm, dọn bàn học hoặc uống một cốc nước.",
        "Đừng ở một mình quá lâu, hãy nhắn tin cho một người bạn hoặc gọi cho người thân.",
        "Hãy tự nói với mình một câu dịu dàng như bạn sẽ nói với một người bạn đang buồn.",
        "Nghe một bản nhạc nhẹ nhàng hoặc một bản nhạc khiến bạn thấy được an ủi.",
        "Chia nhỏ ngày hôm nay thành những việc rất nhỏ, chỉ cần làm xong một việc là đã đủ tốt rồi.",
        "Hãy tránh so sánh mình với người khác, mỗi người có hoàn cảnh và tốc độ riêng.",
        "Nếu cảm thấy buồn kéo dài nhiều ngày, hãy chia sẻ với thầy cô, cha mẹ hoặc chuyên gia tâm lý.",
        "Hãy ăn uống đủ bữa và ngủ đúng giờ, cơ thể được chăm sóc sẽ giúp tinh thần dễ hồi phục hơn.",
        "Viết ra ba điều nhỏ bé vẫn còn tốt đẹp trong ngày hôm nay, dù chỉ là một bữa ăn ngon.",
        "Hãy xem một bộ phim hoặc đọc một cuốn sách nhẹ nhàng để tạm nghỉ khỏi những suy nghĩ nặng nề.",
        "Bạn không cần tự giải quyết mọi thứ một mình, nhờ giúp đỡ là một biểu hiện của sự mạnh mẽ.",
        "Thử vận động nhẹ như giãn cơ, đạp xe hoặc nhảy theo nhạc để giải phóng năng lượng nặng nề.",
        "Hãy ghi lại cảm xúc của mình mỗi ngày để thấy tâm trạng thay đổi theo thời gian.",
        "Hãy chăm sóc một thứ gì đó nhỏ như cây xanh, thú cưng, việc chăm sóc giúp bạn có thêm động lực.",
        "Nếu có nỗi buồn vì mất mát, hãy cho mình thời gian, không có thời hạn nào cho việc buồn cả.",
        "Hãy hạn chế lướt mạng xã hội khi đang buồn, đôi khi nó khiến bạn thấy tệ hơn.",
        "Ngồi cạnh cửa sổ hoặc ra ngoài hít thở không khí trong lành vài phút.",
        "Hãy tìm một hoạt động bạn từng thích như vẽ, chơi nhạc hoặc nấu ăn và làm một chút thôi.",
        "Hãy nhắc mình rằng cảm xúc này rồi sẽ thay đổi, nó không kéo dài mãi mãi.",
        "Gửi một tin nhắn cho người bạn quý và nói rằng hôm nay bạn không ổn, họ sẽ muốn biết.",
        "Thử bài thở nhịp nhàng 4-4 trong Phòng luyện tập để cơ thể dịu lại.",
        "Hãy mặc một bộ quần áo thoải mái và dọn góc ngủ gọn gàng, môi trường dễ chịu giúp tâm trạng nhẹ hơn.",
        "Đừng ép bản thân phải mạnh mẽ, hãy cho mình quyền được mệt và được nghỉ.",
        "Nếu bạn thấy mình không muốn sống hoặc có ý nghĩ làm hại bản thân, hãy nói ngay với người lớn đáng tin cậy hoặc gọi đường dây hỗ trợ tại địa phương.",
        "Hãy dành thời gian cho những người khiến bạn thấy được lắng nghe và an toàn.",
    ],

    "Lo lắng": [
        "Hãy thử hít thở chậm, chia nhỏ vấn đề và tìm người đáng tin cậy để chia sẻ.",
        "Bạn có thể thử bài Thở ra dài 4-6 trong Phòng luyện tập để cơ thể chậm lại khi đầu óc đang lo nghĩ.",
        "Viết ra những điều bạn đang lo, sau đó đánh dấu điều nào bạn có thể làm gì được ngay.",
        "Hãy thử kỹ thuật 5-4-3-2-1: nêu 5 thứ nhìn thấy, 4 thứ chạm được, 3 thứ nghe thấy, 2 thứ ngửi thấy và 1 thứ nếm được.",
        "Chia việc lớn thành những bước nhỏ và chỉ tập trung vào bước đầu tiên.",
        "Hãy tự hỏi: điều này có khả năng xảy ra thật không, và nếu xảy ra thì mình sẽ xử lý như thế nào.",
        "Hãy dành 10 phút mỗi ngày cho thời gian lo lắng, ngoài khoảng đó hãy nhẹ nhàng đưa đầu óc về việc đang làm.",
        "Chia sẻ nỗi lo với bạn bè, người thân hoặc thầy cô, nói ra thường giúp bớt nặng hơn.",
        "Hãy tập trung vào những gì bạn kiểm soát được và buông bớt những điều ngoài tầm tay.",
        "Uống một cốc nước, hạ vai xuống và thả lỏng hàm, cơ thể thả lỏng giúp đầu óc cũng dịu hơn.",
        "Hạn chế cà phê, trà đặc hoặc nước tăng lực nếu bạn thấy tim đập nhanh và bồn chồn.",
        "Chuẩn bị sớm những việc cần thiết như sách vở, giờ giấc, để sáng mai bớt vội vàng.",
        "Đi bộ nhẹ nhàng hoặc giãn cơ vài phút để cơ thể xả bớt năng lượng căng thẳng.",
        "Hãy nhắc mình rằng cảm giác lo lắng sẽ lên đỉnh rồi hạ xuống, bạn không cần chống lại nó.",
        "Hãy thử đếm ngược từ 20 về 0 thật chậm, kết hợp mỗi số với một nhịp thở ra.",
        "Nếu lo lắng về bài kiểm tra, hãy lập kế hoạch ôn tập theo từng ngày thay vì ôn dồn.",
        "Tránh đọc tin hoặc lướt mạng quá nhiều khi đang lo, nó có thể làm nỗi lo lớn hơn.",
        "Hãy nói với bản thân: mình đã chuẩn bị hết sức có thể, phần còn lại không thể kiểm soát hết.",
        "Ngủ đủ giấc là cách rất tốt để giảm lo lắng, hãy tắt màn hình trước giờ ngủ ít nhất 30 phút.",
        "Hãy thử viết thư cho một người bạn tưởng tượng và kể về nỗi lo của mình.",
        "Hãy nhớ lại một lần bạn từng vượt qua khó khăn, bạn có đủ khả năng để làm lại.",
        "Nếu lo lắng làm bạn khó thở hoặc khó ngủ trong nhiều ngày, hãy nói với cha mẹ, thầy cô hoặc chuyên gia tâm lý.",
        "Nghe một bản nhạc êm dịu và tập trung vào từng nhạc cụ trong bản nhạc.",
        "Hãy làm một việc cần dùng tay như xếp đồ, vẽ hoặc nấu ăn để đầu óc nghỉ khỏi suy nghĩ.",
        "Đặt một khoảng thời gian không dùng điện thoại mỗi ngày để đầu óc được yên tĩnh.",
        "Hãy thử thả lỏng từng vùng cơ thể từ ngón chân lên đến đầu, mỗi vùng khoảng vài nhịp thở.",
        "Nói với một người bạn tin tưởng: mình đang lo, bạn có thể ở cạnh mình một chút không.",
        "Hãy viết ra điều tồi tệ nhất có thể xảy ra và cách bạn sẽ ứng phó, thường nó nhỏ hơn bạn tưởng.",
        "Đừng cố đuổi suy nghĩ lo lắng đi, hãy gọi tên nó là mình đang lo rồi quay lại với hơi thở.",
        "Hãy tạo thói quen buổi tối cố định như tắm, đọc sách, hít thở để cơ thể biết đã đến giờ nghỉ.",
        "Bạn không phải đối mặt với nỗi lo một mình, hãy tìm một người sẵn sàng lắng nghe.",
        "Hãy khen bản thân vì đã dám nhìn thẳng vào điều làm mình lo, đó đã là bước đầu quan trọng.",
    ],

    "Căng thẳng": [
        "Bạn nên nghỉ ngơi hợp lý, chia nhỏ công việc và cân bằng thời gian học tập.",
        "Bạn có thể thử bài Siết và thả lỏng cơ trong Phòng luyện tập để giải tỏa sự căng cứng trong người.",
        "Hãy dùng phương pháp 25 phút tập trung và 5 phút nghỉ, rồi lặp lại để không bị quá tải.",
        "Lập danh sách việc cần làm và chọn ra ba việc quan trọng nhất cho hôm nay.",
        "Hãy dừng lại, hít vào chậm 4 giây, thở ra 6 giây, lặp lại 5 lần để cơ thể dịu xuống.",
        "Đừng cố làm tất cả cùng lúc, hãy làm từng việc một và đánh dấu khi hoàn thành.",
        "Ngủ đủ 7 đến 9 giờ mỗi đêm giúp cơ thể và đầu óc phục hồi sau một ngày căng thẳng.",
        "Hãy đứng dậy, vươn vai và đi lại vài phút sau mỗi giờ ngồi học.",
        "Hãy nói với thầy cô hoặc người thân khi khối lượng việc vượt quá khả năng, nhờ hỗ trợ là bình thường.",
        "Dành một khoảng thời gian trong ngày cho sở thích, dù chỉ 15 phút cũng giúp bạn xả hơi.",
        "Hãy ăn uống đủ bữa, tránh bỏ bữa khi bận vì cơ thể thiếu năng lượng sẽ dễ căng thẳng hơn.",
        "Massage nhẹ vùng vai, cổ và thái dương trong vài phút để thả lỏng cơ bắp.",
        "Hãy tắt thông báo điện thoại trong lúc học để giảm bị ngắt quãng và áp lực.",
        "Học cách nói không với những việc không cần thiết để dành sức cho điều quan trọng.",
        "Đi bộ ngoài trời hoặc vận động nhẹ 15 đến 20 phút giúp giảm căng thẳng rõ rệt.",
        "Hãy tự hỏi: việc này có thật sự cần xong ngay hôm nay không, hay có thể để mai.",
        "Sắp xếp góc học tập gọn gàng, môi trường ngăn nắp giúp đầu óc bớt rối.",
        "Hãy tránh thức khuya để học bù thường xuyên, nó khiến bạn căng thẳng nhiều hơn vào hôm sau.",
        "Viết ra những điều đang làm bạn áp lực và gạch bỏ những điều không thuộc quyền kiểm soát của bạn.",
        "Hãy thử bài Quét cơ thể hoặc thở nhịp nhàng 4-4 trong Phòng luyện tập trước khi bắt đầu học.",
        "Chia sẻ với một người bạn đang cùng cảnh ngộ, bạn sẽ thấy mình không đơn độc.",
        "Nghe một bản nhạc không lời nhẹ nhàng khi học để giảm cảm giác nặng nề.",
        "Hãy khen bản thân vì những gì đã làm được, đừng chỉ nhìn vào phần còn thiếu.",
        "Hạn chế đồ uống có caffeine vào buổi chiều và tối để không ảnh hưởng đến giấc ngủ.",
        "Hãy đặt mục tiêu vừa sức, đủ khó để cố gắng nhưng không quá mức khiến bạn kiệt sức.",
        "Dành một buổi trong tuần để nghỉ hoàn toàn, không học, không làm việc.",
        "Uống nước, mở cửa sổ và hít thở không khí mới vài phút khi thấy ngột ngạt.",
        "Hãy nhắc mình rằng điểm số hay kết quả không định nghĩa toàn bộ giá trị của bạn.",
        "Nếu căng thẳng kéo dài làm bạn mất ngủ, đau đầu hoặc không muốn làm gì, hãy nói với cha mẹ, thầy cô hoặc chuyên gia.",
        "Thử một hoạt động sáng tạo như vẽ, viết nhật ký hoặc chơi nhạc để xả căng thẳng.",
        "Hãy lên lịch học xen kẽ môn dễ và môn khó để đầu óc không bị quá tải.",
        "Bạn đang cố gắng rất nhiều, hãy cho mình một khoảng nghỉ xứng đáng.",
    ],

    "Tức giận": [
        "Hãy tạm dừng, hít thở sâu và cho bản thân thời gian bình tĩnh.",
        "Hãy đếm chậm từ 1 đến 10 trước khi nói hoặc làm bất cứ điều gì khi đang tức.",
        "Bạn có thể thử bài Thở nhịp nhàng 4-4 trong Phòng luyện tập để bình tĩnh lại nhanh hơn.",
        "Rời khỏi tình huống một lúc, đi ra chỗ khác hoặc rửa mặt bằng nước mát.",
        "Tránh gửi tin nhắn hoặc đăng bài khi đang giận, hãy chờ đến khi bình tĩnh rồi hãy viết.",
        "Hãy viết ra điều làm bạn tức giận, không cần gửi cho ai, chỉ để giải tỏa.",
        "Vận động mạnh nhẹ như chạy bộ, nhảy dây hoặc đấm gối để xả bớt năng lượng.",
        "Hãy tự hỏi: mình đang giận vì điều gì thật sự, và mình muốn điều gì thay đổi.",
        "Khi đã bình tĩnh, hãy nói cảm xúc của mình bằng câu bắt đầu với chữ mình, ví dụ mình thấy buồn khi bị ngắt lời.",
        "Uống một cốc nước lạnh và hít thở chậm, cơ thể mát hơn thì đầu óc cũng dịu hơn.",
        "Hãy tìm một người bạn tin tưởng để trút bầu tâm sự thay vì giữ trong lòng.",
        "Cố gắng nhìn tình huống từ góc nhìn của người kia, bạn không cần đồng ý nhưng có thể hiểu hơn.",
        "Nếu giận vì thua game hoặc thất bại, hãy nghỉ ngơi một lúc và nhắc mình đó chỉ là một lần chơi.",
        "Hãy tránh nói những lời nặng nề khi đang giận, vì lời nói ra khó lấy lại được.",
        "Nghe một bản nhạc êm dịu hoặc nhạc không lời để hạ nhịp tim.",
        "Hãy thả lỏng vai, mở bàn tay đang nắm chặt và thả lỏng hàm răng.",
        "Hãy ghi lại điều gì thường khiến bạn dễ cáu để nhận ra và chuẩn bị trước.",
        "Đi bộ nhanh 10 phút ngoài trời giúp giải tỏa cơn giận tốt hơn ngồi im.",
        "Đừng giữ cơn giận quá lâu trong lòng, hãy tìm cách nói ra một cách bình tĩnh và tôn trọng.",
        "Hãy nhắc mình rằng tức giận là cảm xúc bình thường, quan trọng là cách bạn hành xử sau đó.",
        "Tạm hoãn các quyết định quan trọng đến khi bạn bình tĩnh trở lại.",
        "Thử vẽ nguệch ngoạc hoặc xé giấy vụn để giải tỏa cảm giác bực dọc.",
        "Hãy ngủ đủ giấc, thiếu ngủ khiến bạn dễ cáu hơn bình thường.",
        "Hãy tránh môi trường hoặc người đang làm bạn khó chịu cho đến khi đã bình tĩnh.",
        "Thở vào bằng mũi 4 giây, thở ra bằng miệng 6 giây, lặp lại cho đến khi nhịp tim chậm lại.",
        "Nếu cơn giận lặp lại thường xuyên, hãy trò chuyện với thầy cô, cha mẹ hoặc chuyên gia tâm lý.",
        "Hãy tưởng tượng bạn đặt cơn giận vào một chiếc hộp rồi tạm cất đi, chờ đến lúc bình tĩnh hãy mở ra.",
        "Làm một việc nhỏ có ích như dọn bàn hoặc sắp xếp sách vở để chuyển hướng năng lượng.",
        "Hãy tự nói: mình có quyền giận, nhưng mình chọn cách phản ứng bình tĩnh.",
        "Bạn có thể xin lỗi nếu lỡ nói quá lời khi giận, điều đó giúp mối quan hệ không bị tổn thương.",
        "Sau khi bình tĩnh, hãy suy nghĩ cách giải quyết vấn đề thay vì chỉ nghĩ đến người có lỗi.",
        "Hãy dành thời gian chăm sóc bản thân, một buổi tối nghỉ ngơi sẽ giúp bạn bình tĩnh hơn.",
    ],
}


# ==========================================
# 3. XU LY TU PHU DINH
# ==========================================

NEGATION_WORDS = [
    "không", "chẳng", "chưa", "đâu có",
    "không hề", "chẳng hề", "không còn",
    "chẳng còn"
]


def is_negated(text, start):
    """
    Kiểm tra từ khóa có đứng sau từ phủ định gần đó không.
    Đây là quy tắc thử nghiệm, chưa hiểu đầy đủ ngữ cảnh.
    """

    prefix = text[max(0, start - 30):start].strip()

    for negation in NEGATION_WORDS:
        if re.search(
            r"(?<!\w)" + re.escape(negation) + r"\s*$",
            prefix
        ):
            return True

    return False


# ==========================================
# 4. PHAN TICH CAM XUC VAN BAN
# ==========================================

def analyze_text(text):
    """
    Phân tích từ khóa cảm xúc trong văn bản tiếng Việt.

    Đây là hệ thống dựa trên từ khóa thử nghiệm,
    chưa phải mô hình AI được huấn luyện.
    """

    if not isinstance(text, str) or not text.strip():
        return {
            "emotion": "Chưa xác định",
            "emotions": [],
            "keywords": [],
            "negated_keywords": [],
            "suggestion": "Vui lòng nhập nội dung để phân tích.",
            "message": "Không có dữ liệu đầu vào."
        }

    normalized_text = re.sub(
        r"\s+", " ", text.lower()
    ).strip()

    emotion_matches = {}
    negated_keywords = []

    for emotion, keywords in EMOTION_KEYWORDS.items():

        matched = []

        for keyword in keywords:
            start = 0

            while True:
                position = normalized_text.find(
                    keyword, start
                )

                if position == -1:
                    break

                if is_negated(normalized_text, position):
                    if keyword not in negated_keywords:
                        negated_keywords.append(keyword)
                else:
                    if keyword not in matched:
                        matched.append(keyword)

                start = position + len(keyword)

        emotion_matches[emotion] = matched

    # Xác định các nhóm cảm xúc được nhận diện
    detected_emotions = [
        emotion
        for emotion, keywords in emotion_matches.items()
        if keywords
    ]

    if not detected_emotions:
        return {
            "emotion": "Chưa xác định",
            "emotions": [],
            "keywords": [],
            "negated_keywords": negated_keywords,
            "suggestion": (
                "Bạn có thể chia sẻ thêm về cảm xúc "
                "hoặc tình huống của mình."
            ),
            "message": "Chưa tìm thấy từ khóa cảm xúc phù hợp."
        }

    # Chọn nhóm có nhiều từ khóa nhất
    primary_emotion = max(
        detected_emotions,
        key=lambda emotion: len(emotion_matches[emotion])
    )

    # Thu thập toàn bộ từ khóa
    all_keywords = [
        keyword
        for emotion in detected_emotions
        for keyword in emotion_matches[emotion]
    ]

    return {
        "emotion": primary_emotion,
        "emotions": detected_emotions,
        "keywords": all_keywords,
        "negated_keywords": negated_keywords,
        "suggestion": random.choice(EMOTION_SUGGESTIONS[primary_emotion]),
        "message": (
            "Đã hoàn thành phân tích từ khóa cảm xúc thử nghiệm."
        )
    }