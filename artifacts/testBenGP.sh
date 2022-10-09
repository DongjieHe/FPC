#!/bin/bash

# for cmd in "./runFineGrainedNGC.py" "./runCleanDroid.py" 
for cmd in "./runFineGrainedNGC.py"
do
## less than 1mins
${cmd} benchmarks/GooglePlayTopFree/active-cleanup-cache-cleaner_1.1.1.apk
${cmd} benchmarks/GooglePlayTopFree/airtel-thanks-recharge-upi_4.55.7.apk
${cmd} benchmarks/GooglePlayTopFree/ajio-online-shopping-app_8.3.3.apk
${cmd} benchmarks/GooglePlayTopFree/bajaj-finserv-upi-pay-loans_7.5.2.apk
${cmd} benchmarks/GooglePlayTopFree/com_flipkart_shopsy_v7.17.apk
${cmd} benchmarks/GooglePlayTopFree/facebook_332.0.0.23.111.apk
${cmd} benchmarks/GooglePlayTopFree/facebook-lite_323.0.0.9.106.apk
${cmd} benchmarks/GooglePlayTopFree/fast-cleaner-cpu-cooler_1.1.4.apk
${cmd} benchmarks/GooglePlayTopFree/flipkart-online-shopping-app_7.52.apk
${cmd} benchmarks/GooglePlayTopFree/google-pay-save-pay-manage_163.1.6arm64v8a_release_flutter.apk
${cmd} benchmarks/GooglePlayTopFree/in_amazon_mshop_android_shopping_v24.18.0.300.apk
${cmd} benchmarks/GooglePlayTopFree/instagram_256.0.0.12.105.apk
${cmd} benchmarks/GooglePlayTopFree/instagram-lite_323.0.0.9.106.apk
${cmd} benchmarks/GooglePlayTopFree/jiosaavn-music-podcasts_8.14.1.apk
${cmd} benchmarks/GooglePlayTopFree/jiotv_7.0.7.apk
${cmd} benchmarks/GooglePlayTopFree/mast-music-status-video-maker_1.5.4.apk
${cmd} benchmarks/GooglePlayTopFree/meesho-online-shopping-app_13.6.apk
${cmd} benchmarks/GooglePlayTopFree/mivita-face-swap-video-maker_1.1.6.apk
${cmd} benchmarks/GooglePlayTopFree/mx-player_1.51.1.apk
${cmd} benchmarks/GooglePlayTopFree/myjio-for-everything-jio_7.0.21.apk
${cmd} benchmarks/GooglePlayTopFree/noizz-video-editor-with-music_5.6.1.apk
${cmd} benchmarks/GooglePlayTopFree/normalproxy-fast-stable-safe_1.2.1.apk
${cmd} benchmarks/GooglePlayTopFree/paytm-secure-upi-payments_9.13.7.apk
${cmd} benchmarks/GooglePlayTopFree/phonepe-upi-payment-recharge_4.1.40.apk
${cmd} benchmarks/GooglePlayTopFree/playit-all-in-one-video-player_2.6.4.46.apk
${cmd} benchmarks/GooglePlayTopFree/public-indian-local-videos_2.39.1.apk
${cmd} benchmarks/GooglePlayTopFree/purplle-online-beauty-shopping_2.0.90.apk
${cmd} benchmarks/GooglePlayTopFree/resso-music-songs-lyrics_1.94.0.apk
${cmd} benchmarks/GooglePlayTopFree/sharechat-made-in-india_17.8.11.apk
${cmd} benchmarks/GooglePlayTopFree/share-karo-file-transfer-app_2.2.29.apk
${cmd} benchmarks/GooglePlayTopFree/shareme-file-sharing_3.28.10.apk
${cmd} benchmarks/GooglePlayTopFree/snapchat_12.04.0.25beta.apk
${cmd} benchmarks/GooglePlayTopFree/spotify-music-and-podcasts_8.7.72.546.apk
${cmd} benchmarks/GooglePlayTopFree/telegram_9.0.2.apk
${cmd} benchmarks/GooglePlayTopFree/truecaller-caller-id-block_12.48.6.apk
${cmd} benchmarks/GooglePlayTopFree/vi-recharge-music-games-tv_9.7.9.apk
${cmd} benchmarks/GooglePlayTopFree/voot-bigg-boss-colors-tv_4.4.9.apk
${cmd} benchmarks/GooglePlayTopFree/vpn-go-private-net-access_1.0.25.apk
${cmd} benchmarks/GooglePlayTopFree/whatsapp-business_2.22.20.79.apk
${cmd} benchmarks/GooglePlayTopFree/whatsapp-messenger_2.22.20.79.apk
${cmd} benchmarks/GooglePlayTopFree/where-is-my-train_7.1.3.apk
${cmd} benchmarks/GooglePlayTopFree/wynk-music-songs-podcasts-mp3_3.36.1.3.apk
${cmd} benchmarks/GooglePlayTopFree/zee5-movies-tv-shows-series_38.5.6.apk
${cmd} benchmarks/GooglePlayTopFree/zomato-food-delivery-dining_17.0.5.apk


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
