#!/usr/bin/env python3
import os

run = "output/"
FLOWDROID = "./driver.py -out=" + run + "FD1"
CLEANDROID = "./driver.py -solver=GC -out=" + run + "GC1 -st=1"
CLEANDROID2 = "./driver.py -solver=GC -out=" + run + "GC2 -st=2"
CLEANDROID3 = "./driver.py -solver=GC -out=" + run + "GC3 -st=3"
CLEANDROID4 = "./driver.py -solver=GC -out=" + run + "GC4 -st=4"
CLEANDROID5 = "./driver.py -solver=GC -out=" + run + "GC5 -st=5"
CLEANDROID6 = "./driver.py -solver=GC -out=" + run + "GC6 -st=6"
CLEANDROID7 = "./driver.py -solver=GC -out=" + run + "GC7 -st=7"
CLEANDROID8 = "./driver.py -solver=GC -out=" + run + "GC8 -st=8"
FPC = "./driver.py -solver=FPC -out=" + run + "FPC1 -st=1"
FPC2 = "./driver.py -solver=FPC -out=" + run + "FPC2 -st=2"
FPC3 = "./driver.py -solver=FPC -out=" + run + "FPC3 -st=3"
FPC4 = "./driver.py -solver=FPC -out=" + run + "FPC4 -st=4"
FPC5 = "./driver.py -solver=FPC -out=" + run + "FPC5 -st=5"
FPC6 = "./driver.py -solver=FPC -out=" + run + "FPC6 -st=6"
FPC7 = "./driver.py -solver=FPC -out=" + run + "FPC7 -st=7"
FPC8 = "./driver.py -solver=FPC -out=" + run + "FPC8 -st=8"

TOOLS = [FLOWDROID, FPC, CLEANDROID, FPC2, FPC3, FPC4, FPC5, FPC6, FPC7, FPC8, CLEANDROID2,
         CLEANDROID3, CLEANDROID4, CLEANDROID5, CLEANDROID6, CLEANDROID7, CLEANDROID8]

appPaths = [
    #############################################################################################################
    # Section 1: apps could either be analyzed within 1 or 2 seconds or run into crash by FlowDroid.

    # crashed.
    # benchmarks/sparsedroidBenchmark/ca.cmetcalfe.locationshare.apk
    # benchmarks/sparsedroidBenchmark/com.orgzly_1.7.apk
    # benchmarks/sparsedroidBenchmark/de.schildbach.oeffi_10.5.3-google.apk
    # benchmarks/sparsedroidBenchmark/eu.faircode.netguard_2.229.apk
    # benchmarks/diskDroidBenchmarks/group2/fr.gouv.etalab.mastodon_345.apk
    # benchmarks/sparsedroidBenchmark/org.adw.launcher_1.3.6.apk
    # benchmarks/diskDroidBenchmarks/group2/org.smssecure.smssecure_211.apk
    # benchmarks/diskDroidBenchmarks/group1/org.yaxim.androidclient_53.apk
    # benchmarks/sparsedroidBenchmark/uk.co.richyhbm.monochromatic.apk

    # small apps.
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

    # less than 1mins
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
    # benchmarks/sparsedroidBenchmark/org.gateshipone.odyssey_1.1.17.apk # newer version exists in diskDroidBenchmarks
    'benchmarks/sparsedroidBenchmark/org.materialos.icons_2.1.apk',

    # 1 to 10 mins
    'benchmarks/diskDroidBenchmarks/group1/org.fdroid.fdroid_1008000.apk',
    'benchmarks/diskDroidBenchmarks/group2/com.kanedias.vanilla.metadata_5.apk',
    'benchmarks/diskDroidBenchmarks/group3/com.genonbeta.TrebleShot_98.apk',
    # benchmarks/sparsedroidBenchmark/com.github.axet.callrecorder_1.6.44.apk # newer version exists in diskDroidBenchmarks
    'benchmarks/sparsedroidBenchmark/com.igisw.openmoneybox.3.4.1.8.apk',
    'benchmarks/sparsedroidBenchmark/com.vonglasow.michael.satstat.apk',
    'benchmarks/sparsedroidBenchmark/name.myigel.fahrplan.eh17_1.33.16.apk',
    'benchmarks/sparsedroidBenchmark/org.secuso.privacyfriendlytodolist_2.1.apk',
    'benchmarks/sparsedroidBenchmark/org.totschnig.myexpenses.apk',
    'benchmarks/sparsedroidBenchmark/com.adobe.reader_19.2.1.9183.apk',
    'benchmarks/sparsedroidBenchmark/com.microsoft.office.word_16.0.11425.20132.apk',
    'benchmarks/sparsedroidBenchmark/com.emn8.mobilem8.nativeapp.bk_5.0.10.apk',

    # 10 to 30 mins

    # more than 30 mins-1 hour.
    'benchmarks/diskDroidBenchmarks/group1/org.lumicall.android_190.apk',
    'benchmarks/diskDroidBenchmarks/group1/nya.miku.wishmaster_54.apk',
    # more than 1 hour
    # benchmarks/sparsedroidBenchmark/nya.miku.wishmaster.apk # newer version exists in diskDroidBenchmarks
    'benchmarks/diskDroidBenchmarks/group1/bus.chio.wishmaster_1002.apk',
    #######################

    # about 2 hours
    'benchmarks/diskDroidBenchmarks/group2/com.github.axet.bookreader_375.apk',
    'benchmarks/sparsedroidBenchmark/org.openpetfoodfacts.scanner_2.9.8.apk',

    ########################################################################################################################################
    # Section 3: apps which either run out of memory or could not be analyzed within the given budget. Should be consided in the future.
    # run on a machine with more than 500GB memory.
    # more than 3 hours
    # 'benchmarks/sparsedroidBenchmark/com.ichi2.anki_2.8.4.apk',
    # more than 5 hours
    # 'benchmarks/sparsedroidBenchmark/com.microsoft.office.outlook_3.0.46.apk',
    # 'benchmarks/sparsedroidBenchmark/com.nianticlabs.pokemongo_0.139.3.apk',
    # 'benchmarks/diskDroidBenchmarks/group3/de.k3b.android.androFotoFinder_44.apk',
    # still out of memory.
    # benchmarks/diskDroidBenchmarks/group1/F-Droid.apk
    ##########################

    ########################################################################################################
    # TaintBench
    # within 0 seconds
    # 'benchmarks/TaintBench/the_interview_movieshow.apk',
    # 'benchmarks/TaintBench/fakeplay.apk',
    # 'benchmarks/TaintBench/overlay_android_samp.apk',
    # 'benchmarks/TaintBench/exprespam.apk',
    # 'benchmarks/TaintBench/phospy.apk',
    # 'benchmarks/TaintBench/smsstealer_kysn_assassincreed_android_samp.apk',
    # 'benchmarks/TaintBench/beita_com_beita_contact.apk',
    # 'benchmarks/TaintBench/sms_google.apk',
    # 'benchmarks/TaintBench/xbot_android_samp.apk',
    # 'benchmarks/TaintBench/jollyserv.apk',
    # 'benchmarks/TaintBench/proxy_samp.apk',
    # 'benchmarks/TaintBench/scipiex.apk',
    # 'benchmarks/TaintBench/tetus.apk',
    # 'benchmarks/TaintBench/threatjapan_uracto.apk',
    # 'benchmarks/TaintBench/fakedaum.apk',
    # 'benchmarks/TaintBench/chat_hook.apk',
    # 'benchmarks/TaintBench/roidsec.apk',
    # 'benchmarks/TaintBench/faketaobao.apk',
    # 'benchmarks/TaintBench/overlaylocker2_android_samp.apk',
    # 'benchmarks/TaintBench/hummingbad_android_samp.apk',
    # 'benchmarks/TaintBench/vibleaker_android_samp.apk',
    # 'benchmarks/TaintBench/backflash.apk',
    # 'benchmarks/TaintBench/cajino_baidu.apk',
    # 'benchmarks/TaintBench/save_me.apk',
    # 'benchmarks/TaintBench/remote_control_smack.apk',
    # 'benchmarks/TaintBench/smssend_packageInstaller.apk',
    # 'benchmarks/TaintBench/stels_flashplayer_android_update.apk',

    # crash or no sources
    # 'benchmarks/TaintBench/sms_send_locker_qqmagic.apk',
    # 'benchmarks/TaintBench/chulia.apk',
    # 'benchmarks/TaintBench/fakebank_android_samp.apk',
    # 'benchmarks/TaintBench/godwon_samp.apk',
    # 'benchmarks/TaintBench/fakeappstore.apk',
    # 'benchmarks/TaintBench/repane.apk',
    # 'benchmarks/TaintBench/fakemart.apk',
    # 'benchmarks/TaintBench/samsapo.apk',
    # 'benchmarks/TaintBench/slocker_android_samp.apk',
    # 'benchmarks/TaintBench/death_ring_materialflow.apk',
    # 'benchmarks/TaintBench/dsencrypt_samp.apk',
    # 'benchmarks/TaintBench/smssilience_fake_vertu.apk',
]

UNSCALABLE = {
    'FLOWDROID': ['benchmarks/diskDroidBenchmarks/group1/bus.chio.wishmaster_1002.apk', 'benchmarks/diskDroidBenchmarks/group2/com.github.axet.bookreader_375.apk',
                  'benchmarks/sparsedroidBenchmark/org.openpetfoodfacts.scanner_2.9.8.apk'],
    'CLEANDROID': ['benchmarks/diskDroidBenchmarks/group1/bus.chio.wishmaster_1002.apk', 'benchmarks/diskDroidBenchmarks/group2/com.github.axet.bookreader_375.apk',
                   'benchmarks/sparsedroidBenchmark/org.openpetfoodfacts.scanner_2.9.8.apk'],
    'FPC': []
}

for tool in TOOLS:
    for appPath in appPaths:
        if appPath in UNSCALABLE['FLOWDROID'] and '-solver=' not in tool:
            print(appPath + " is unscalable under flowdroid!")
        if appPath in UNSCALABLE['CLEANDROID'] and '-solver=GC' in tool:
            print(appPath + " is unscalable under cleandroid!")
        elif appPath in UNSCALABLE['FPC'] and '-solver=FINEGRAIN' in tool:
            print(appPath + " is unscalable under FPC!")
        elif appPath in UNSCALABLE['CLEANDROID'] and tool in [FPC2, FPC3, FPC4, FPC5, FPC6, FPC7, FPC8]:
            print(appPath + " is unscalable under cleandroid thus do not need to run")
        else:
            os.system(tool + ' ' + appPath)
