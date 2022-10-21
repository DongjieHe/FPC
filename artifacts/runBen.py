#!/usr/bin/env python3
import os

FPC = "./run.py -solver=FINEGRAIN -out=run6"
CLEANDROID = "./run.py -solver=GC -out=run6"
CLEANDROID4 = "./run.py -solver=GC -out=run6 -st=4"
# FPC0 = "./run.py -solver=FINEGRAIN -out=run6/FPC0 -st=0"
FPC2 = "./run.py -solver=FINEGRAIN -out=run6/FPC2 -st=2"
FPC3 = "./run.py -solver=FINEGRAIN -out=run6/FPC3 -st=3"
FPC4 = "./run.py -solver=FINEGRAIN -out=run6/FPC4 -st=4"
FPC5 = "./run.py -solver=FINEGRAIN -out=run6/FPC5 -st=5"
FPC6 = "./run.py -solver=FINEGRAIN -out=run6/FPC6 -st=6"
FPC7 = "./run.py -solver=FINEGRAIN -out=run6/FPC7 -st=7"
FPC8 = "./run.py -solver=FINEGRAIN -out=run6/FPC8 -st=8"
TOOLS = [FPC, CLEANDROID, FPC2, FPC3, FPC4, FPC5, FPC6, FPC7, FPC8, CLEANDROID4]

# for cmd in "./runFineGrainedNGC.py" "./runCleanDroid.py" 
# for cmd in "./runFineGrainedNGC.py"
# do
appPaths = [
#############################################################################################################
# Section 1: apps could either be analyzed within 1 or 2 seconds or run into crash by FlowDroid.

## crashed.
# benchmarks/sparsedroidBenchmark/ca.cmetcalfe.locationshare.apk
# benchmarks/sparsedroidBenchmark/com.orgzly_1.7.apk
# benchmarks/sparsedroidBenchmark/de.schildbach.oeffi_10.5.3-google.apk
# benchmarks/sparsedroidBenchmark/eu.faircode.netguard_2.229.apk
# benchmarks/diskDroidBenchmarks/group2/fr.gouv.etalab.mastodon_345.apk
# benchmarks/sparsedroidBenchmark/org.adw.launcher_1.3.6.apk
# benchmarks/diskDroidBenchmarks/group2/org.smssecure.smssecure_211.apk
# benchmarks/diskDroidBenchmarks/group1/org.yaxim.androidclient_53.apk
# benchmarks/sparsedroidBenchmark/uk.co.richyhbm.monochromatic.apk

## small apps.
# benchmarks/sparsedroidBenchmark/be.mygod.vpnhotspot.apk
# benchmarks/sparsedroidBenchmark/com.ghstudios.android.mhgendatabase.apk
# benchmarks/sparsedroidBenchmark/com.luk.timetable2_6.0.4_28.apk
# benchmarks/sparsedroidBenchmark/com.poupa.vinylmusicplayer_0.20.1.apk
# benchmarks/sparsedroidBenchmark/de.k3b.android.contentproviderhelper.apk
# benchmarks/diskDroidBenchmarks/group1/hashengineering.groestlcoin.wallet_71107.apk
# benchmarks/sparsedroidBenchmark/nightlock-peppercarrot.apk
# benchmarks/sparsedroidBenchmark/org.secuso.privacyfriendlyactivitytracker_1.0.5.apk
# benchmarks/sparsedroidBenchmark/rodrigodavy.com.github.pixelartist.apk
# benchmarks/sparsedroidBenchmark/acr.browser.lightning_4.5.1.apk
# benchmarks/diskDroidBenchmarks/group3/com.zeapo.pwdstore_10303.apk
# benchmarks/sparsedroidBenchmark/net.ddns.mlsoftlaberge.trycorder.apk
# benchmarks/sparsedroidBenchmark/opencontacts.open.com.opencontacts_12.apk
###########################################################################################################################################
# Section 2: apps that could successfully analyzed by fine-grained aggressive analysis by us.

## less than 1mins
'benchmarks/diskDroidBenchmarks/group1/com.alfray.timeriffic_10905.apk', 
'benchmarks/diskDroidBenchmarks/group1/org.gateshipone.odyssey_30.apk',
'benchmarks/diskDroidBenchmarks/group2/org.secuso.privacyfriendlyweather_6.apk',
'benchmarks/diskDroidBenchmarks/group3/com.github.axet.callrecorder_219.apk',
'benchmarks/sparsedroidBenchmark/com.app.Zensuren_1.21.apk',
'benchmarks/sparsedroidBenchmark/com.github.yeriomin.dumbphoneassistant_5.apk',
'benchmarks/sparsedroidBenchmark/com.ilm.sandwich_2.2.4f.apk',
'benchmarks/sparsedroidBenchmark/com.kunzisoft.keepass.libre_2.5.0.0beta18.apk',
'benchmarks/sparsedroidBenchmark/dk.jens.backup_0.3.4.apk',
'benchmarks/sparsedroidBenchmark/org.csploit.android.apk',
'benchmarks/sparsedroidBenchmark/org.decsync.sparss.floss_1.13.4.apk',
# benchmarks/sparsedroidBenchmark/org.gateshipone.odyssey_1.1.17.apk
'benchmarks/sparsedroidBenchmark/org.materialos.icons_2.1.apk',

## 1 to 10 mins
'benchmarks/diskDroidBenchmarks/group1/org.fdroid.fdroid_1008000.apk',
'benchmarks/diskDroidBenchmarks/group2/com.kanedias.vanilla.metadata_5.apk',
'benchmarks/diskDroidBenchmarks/group3/com.genonbeta.TrebleShot_98.apk',
# benchmarks/sparsedroidBenchmark/com.github.axet.callrecorder_1.6.44.apk
'benchmarks/sparsedroidBenchmark/com.igisw.openmoneybox.3.4.1.8.apk',
'benchmarks/sparsedroidBenchmark/com.vonglasow.michael.satstat.apk',
'benchmarks/sparsedroidBenchmark/name.myigel.fahrplan.eh17_1.33.16.apk',
'benchmarks/sparsedroidBenchmark/org.secuso.privacyfriendlytodolist_2.1.apk',
'benchmarks/sparsedroidBenchmark/org.totschnig.myexpenses.apk',
'benchmarks/sparsedroidBenchmark/com.adobe.reader_19.2.1.9183.apk',
'benchmarks/sparsedroidBenchmark/com.microsoft.office.word_16.0.11425.20132.apk',
'benchmarks/sparsedroidBenchmark/com.emn8.mobilem8.nativeapp.bk_5.0.10.apk',

## 10 to 30 mins

## more than 30 mins-1 hour.
'benchmarks/diskDroidBenchmarks/group1/org.lumicall.android_190.apk',
'benchmarks/diskDroidBenchmarks/group1/nya.miku.wishmaster_54.apk',
## more than 1 hour
# benchmarks/sparsedroidBenchmark/nya.miku.wishmaster.apk
# 'benchmarks/diskDroidBenchmarks/group1/bus.chio.wishmaster_1002.apk',
#######################

# about 2 hours
# 'benchmarks/diskDroidBenchmarks/group2/com.github.axet.bookreader_375.apk',
# 'benchmarks/sparsedroidBenchmark/org.openpetfoodfacts.scanner_2.9.8.apk',

########################################################################################################################################
# Section 3: apps which either run out of memory or could not be analyzed within the given budget. Should be consided in the future.

# more than 3 hours
# ${cmd} benchmarks/sparsedroidBenchmark/com.ichi2.anki_2.8.4.apk
# more than 5 hours
# benchmarks/sparsedroidBenchmark/com.microsoft.office.outlook_3.0.46.apk
# benchmarks/sparsedroidBenchmark/com.nianticlabs.pokemongo_0.139.3.apk
# benchmarks/diskDroidBenchmarks/group3/de.k3b.android.androFotoFinder_44.apk
# still out of memory.
# benchmarks/diskDroidBenchmarks/group1/F-Droid.apk 
##########################
]
# done

for tool in TOOLS:
    for appPath in appPaths:
        os.system(tool + ' ' + appPath)
