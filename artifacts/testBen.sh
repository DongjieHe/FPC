#!/bin/bash

# cmd="./runCleanDroid.py"
# cmd="./runFineGrainedAGC.py"
# cmd="./runFineGrainedNGC.py"
cmd="./runFlowDroid.py"

#############################################################################################################
# Section 1: apps could either be analyzed within 1 or 2 seconds or run into crash by FlowDroid.

## crashed.
#${cmd} benchmarks/sparsedroidBenchmark/ca.cmetcalfe.locationshare.apk
#${cmd} benchmarks/sparsedroidBenchmark/com.orgzly_1.7.apk
#${cmd} benchmarks/sparsedroidBenchmark/de.schildbach.oeffi_10.5.3-google.apk
#${cmd} benchmarks/sparsedroidBenchmark/eu.faircode.netguard_2.229.apk
#${cmd} benchmarks/diskDroidBenchmarks/group2/fr.gouv.etalab.mastodon_345.apk
#${cmd} benchmarks/sparsedroidBenchmark/org.adw.launcher_1.3.6.apk
#${cmd} benchmarks/diskDroidBenchmarks/group2/org.smssecure.smssecure_211.apk
#${cmd} benchmarks/diskDroidBenchmarks/group1/org.yaxim.androidclient_53.apk
#${cmd} benchmarks/sparsedroidBenchmark/uk.co.richyhbm.monochromatic.apk

## small apps.
#${cmd} benchmarks/sparsedroidBenchmark/be.mygod.vpnhotspot.apk
#${cmd} benchmarks/sparsedroidBenchmark/com.ghstudios.android.mhgendatabase.apk
#${cmd} benchmarks/sparsedroidBenchmark/com.luk.timetable2_6.0.4_28.apk
#${cmd} benchmarks/sparsedroidBenchmark/com.poupa.vinylmusicplayer_0.20.1.apk
#${cmd} benchmarks/sparsedroidBenchmark/de.k3b.android.contentproviderhelper.apk
#${cmd} benchmarks/diskDroidBenchmarks/group1/hashengineering.groestlcoin.wallet_71107.apk
#${cmd} benchmarks/sparsedroidBenchmark/nightlock-peppercarrot.apk
#${cmd} benchmarks/sparsedroidBenchmark/org.secuso.privacyfriendlyactivitytracker_1.0.5.apk
#${cmd} benchmarks/sparsedroidBenchmark/rodrigodavy.com.github.pixelartist.apk
#${cmd} benchmarks/sparsedroidBenchmark/acr.browser.lightning_4.5.1.apk
#${cmd} benchmarks/diskDroidBenchmarks/group3/com.zeapo.pwdstore_10303.apk
#${cmd} benchmarks/sparsedroidBenchmark/net.ddns.mlsoftlaberge.trycorder.apk
#${cmd} benchmarks/sparsedroidBenchmark/opencontacts.open.com.opencontacts_12.apk
###########################################################################################################################################
# Section 2: apps that could successfully analyzed by fine-grained aggressive analysis by us.

## less than 1mins
${cmd} benchmarks/diskDroidBenchmarks/group1/com.alfray.timeriffic_10905.apk
${cmd} benchmarks/diskDroidBenchmarks/group1/org.gateshipone.odyssey_30.apk
${cmd} benchmarks/diskDroidBenchmarks/group2/org.secuso.privacyfriendlyweather_6.apk
${cmd} benchmarks/diskDroidBenchmarks/group3/com.github.axet.callrecorder_219.apk
${cmd} benchmarks/sparsedroidBenchmark/com.app.Zensuren_1.21.apk
${cmd} benchmarks/sparsedroidBenchmark/com.github.yeriomin.dumbphoneassistant_5.apk
${cmd} benchmarks/sparsedroidBenchmark/com.ilm.sandwich_2.2.4f.apk
${cmd} benchmarks/sparsedroidBenchmark/com.kunzisoft.keepass.libre_2.5.0.0beta18.apk
${cmd} benchmarks/sparsedroidBenchmark/dk.jens.backup_0.3.4.apk
${cmd} benchmarks/sparsedroidBenchmark/org.csploit.android.apk
${cmd} benchmarks/sparsedroidBenchmark/org.decsync.sparss.floss_1.13.4.apk
# ${cmd} benchmarks/sparsedroidBenchmark/org.gateshipone.odyssey_1.1.17.apk
${cmd} benchmarks/sparsedroidBenchmark/org.materialos.icons_2.1.apk

## 1 to 10 mins
${cmd} benchmarks/diskDroidBenchmarks/group1/org.fdroid.fdroid_1008000.apk
${cmd} benchmarks/diskDroidBenchmarks/group2/com.kanedias.vanilla.metadata_5.apk
${cmd} benchmarks/diskDroidBenchmarks/group3/com.genonbeta.TrebleShot_98.apk
# ${cmd} benchmarks/sparsedroidBenchmark/com.github.axet.callrecorder_1.6.44.apk
${cmd} benchmarks/sparsedroidBenchmark/com.igisw.openmoneybox.3.4.1.8.apk
${cmd} benchmarks/sparsedroidBenchmark/com.vonglasow.michael.satstat.apk
${cmd} benchmarks/sparsedroidBenchmark/name.myigel.fahrplan.eh17_1.33.16.apk
${cmd} benchmarks/sparsedroidBenchmark/org.secuso.privacyfriendlytodolist_2.1.apk
${cmd} benchmarks/sparsedroidBenchmark/org.totschnig.myexpenses.apk
${cmd} benchmarks/sparsedroidBenchmark/com.adobe.reader_19.2.1.9183.apk
${cmd} benchmarks/sparsedroidBenchmark/com.microsoft.office.word_16.0.11425.20132.apk
${cmd} benchmarks/sparsedroidBenchmark/com.emn8.mobilem8.nativeapp.bk_5.0.10.apk

## 10 to 30 mins

## more than 30 mins-1 hour.
${cmd} benchmarks/diskDroidBenchmarks/group1/org.lumicall.android_190.apk
${cmd} benchmarks/diskDroidBenchmarks/group1/nya.miku.wishmaster_54.apk
## more than 1 hour
# ${cmd} benchmarks/sparsedroidBenchmark/nya.miku.wishmaster.apk
${cmd} benchmarks/diskDroidBenchmarks/group1/bus.chio.wishmaster_1002.apk
#######################

# about 2 hours
${cmd} benchmarks/diskDroidBenchmarks/group2/com.github.axet.bookreader_375.apk
${cmd} benchmarks/sparsedroidBenchmark/org.openpetfoodfacts.scanner_2.9.8.apk

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
