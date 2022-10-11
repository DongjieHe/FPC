#!/bin/bash

# for cmd in "./runFineGrainedNGC.py" "./runCleanDroid.py" 
for cmd in "./runFineGrainedNGC.py"
do
## less than 1mins
${cmd} adobe-scan-pdf-scanner-ocr_22.08.29regular.apk
${cmd} AF3DWBfkGpzLDiMDFxTo4XhicYUCStAldu_bYSMV_CIXaT0cwiqg7kSg0JnembJc9HrGb8qxuEbJVHcsYGbrpGivmY2FaWpjvNaXuROPaQg_kTN7L3wjJWhBpyywh-I7xF7Fm5ByBAfydYTF6ljVHgV5rrgFlhtL-w.apk
${cmd} AF3DWBfkGpzLDiMDFxTo4XhicYUCStAldu_bYSMV_CIXaT0cwl2xBz__ZCQpqtsCuXmZpx9yOL4TzJKwGCzm6gbeZPa7vyBUgFmQQfbhflAL4v58aWa13UtA1IYbEZIZESg-w3Y7cmuxRb-AtXc3a_5TJgnOU03WMw.apk
${cmd} AF3DWBfkGpzLDiMDFxTo4XhicYUCStAldu_bYSMV_CIXaT0cwtHxUpaOofSqkETzX5T_ndBB0mZarWWXiPYSUaDoZj0HmA6mbXQ4xy_hl6QKzl9fSz4vNrGmxKFf4tOAWNL9WHwE4gqtlujgxYr0jNvU2Olx3DEniQ.apk
${cmd} AF3DWBfkGpzLDiMDFxTo4XhicYUCStAldu_bYSMV_CIXaT0cwv5KC4A8iFMcFTWFq21XKaD8o9qMXt9kU_y-foBGPdmxLBV8ysE6bY4dqawaI93J6RKOU8tFFcMSx2lkgnHh3qSZWcIGU-_ZH6-Ofz0ZDnApgzeAXg.apk
${cmd} amazon-seller-sell-on-amazon_8.2.0.apk
${cmd} atom-meditation-for-beginners_1.13.16.apk
${cmd} bandcamp_2.5.5.apk
${cmd} blinkit-grocery-in-minutes_14.16.0.1.apk
${cmd} bumble-dating-friends-bizz_5.289.0.apk
${cmd} canva-design-photo-video_2.186.0.apk
${cmd} fachat-online-video-chat_1.0.5547.apk
${cmd} fitnotes-gym-workout-log_1.23.1.apk
${cmd} glassdoor-jobs-search-more_6.5.0.apk
${cmd} glassdoor-jobs-search-more_9.5.0.apk
${cmd} google-drive_2.19.412.05.44.apk
${cmd} google-one_1.63.309504111.apk
${cmd} grindr-gay-chat_8.19.1.apk
${cmd} headspace-mindful-meditation_4.119.2.apk
${cmd} hinow-private-video-chat_4.4.3.64.apk
${cmd} h-m-we-love-fashion_22.37.2.apk
${cmd} honeycam-chat-live-video-chat_1.19.6.apk
${cmd} intellect-create-a-better-you_2.2.6.apk
${cmd} khan-academy_7.6.1.apk
${cmd} linkedin-jobs-business-news_4.1.742.apk
${cmd} lumi-online-video-chat_1.0.4650.apk
${cmd} medito-meditation-sleep_2.0.48.apk
${cmd} mumu-india-1-on-1-video-chat_1.0.4228.apk
${cmd} mumu-random-video-chat_1.0.4227.apk
${cmd} parau-video-chat-with-friends_1.0.4236.apk
${cmd} paypal-honey-coupons-rewards_3.11.0.apk
${cmd} pdf-reader-pdf-viewer-2022_1.2.4.apk
${cmd} perfect-ear-music-rhythm_3.9.36.apk
${cmd} picsart-color-painting-draw_2.9.apk
${cmd} pocket-save-read-grow_7.64.1.0.apk
${cmd} scribd-audiobooks-ebooks_12.20.apk
${cmd} shopping-list_5.6.apk
${cmd} smiling-mind_4.12.4.apk
${cmd} stitcher-podcast-player_10.35.867.apk
${cmd} storytel-audiobooks-ebooks_22.37.apk
${cmd} superlive_1.10.1.apk
${cmd} tiki-short-video-app_3.11.1.apk
${cmd} tradingview-track-all-markets_1.18.4.2.776.apk
${cmd} udemy-online-courses_8.6.1.apk
${cmd} ullu_2.9.906.apk
${cmd} waking-up-guided-meditation_2.8.1.apk
${cmd} wizdom-self-growth-challenge_8.4.1.apk


########################################################################################################################################
# Section 3: apps which either run out of memory or could not be analyzed within the given budget. Should be consided in the future.

# more than 3 hours
# ${cmd} benchmarks/sparsedroidBenchmark/com.ichi2.anki_2.8.4.apk
# more than 5 hours
# ${cmd} benchmarks/sparsedroidBenchmark/com.microsoft.office.outlook_3.0.46.apk
# ${cmd} benchmarks/sparsedroidBenchmark/com.nianticlabs.pokemongo_0.139.3.apk
# ${cmd} benchmarks/diskDroidBenchmarks/group3/de.k3b.android.androFotoFinder_44.apk

# run out of 256 GB
# ${cmd} benchmarks/diskDroidBenchmarks/group1/F-Droid.apk # AGC, NGC, FLOWDROID, GC
##########################
done
