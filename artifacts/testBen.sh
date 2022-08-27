#!/bin/bash

#############################################################################################################
# Section 1: apps could either be analyzed within 1 or 2 seconds or run into crash by FlowDroid.

## crashed.
echo "analyzing benchmarks/sparsedroidBenchmark/ca.cmetcalfe.locationshare.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/ca.cmetcalfe.locationshare.apk > ca.cmetcalfe.locationshare.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/com.orgzly_1.7.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/com.orgzly_1.7.apk > com.orgzly_1.7.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/de.schildbach.oeffi_10.5.3-google.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/de.schildbach.oeffi_10.5.3-google.apk > de.schildbach.oeffi_10.5.3-google.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/eu.faircode.netguard_2.229.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/eu.faircode.netguard_2.229.apk > eu.faircode.netguard_2.229.log 2>&1

echo "analyzing benchmarks/diskDroidBenchmarks/group2/fr.gouv.etalab.mastodon_345.apk"
./runSingle.py benchmarks/diskDroidBenchmarks/group2/fr.gouv.etalab.mastodon_345.apk > fr.gouv.etalab.mastodon_345.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/org.adw.launcher_1.3.6.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/org.adw.launcher_1.3.6.apk > org.adw.launcher_1.3.6.log 2>&1

echo "analyzing benchmarks/diskDroidBenchmarks/group2/org.smssecure.smssecure_211.apk"
./runSingle.py benchmarks/diskDroidBenchmarks/group2/org.smssecure.smssecure_211.apk > org.smssecure.smssecure_211.log 2>&1

echo "analyzing benchmarks/diskDroidBenchmarks/group1/org.yaxim.androidclient_53.apk"
./runSingle.py benchmarks/diskDroidBenchmarks/group1/org.yaxim.androidclient_53.apk > org.yaxim.androidclient_53.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/uk.co.richyhbm.monochromatic.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/uk.co.richyhbm.monochromatic.apk > uk.co.richyhbm.monochromatic.log 2>&1

## small apps.
echo "analyzing benchmarks/sparsedroidBenchmark/be.mygod.vpnhotspot.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/be.mygod.vpnhotspot.apk > be.mygod.vpnhotspot.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/com.ghstudios.android.mhgendatabase.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/com.ghstudios.android.mhgendatabase.apk > com.ghstudios.android.mhgendatabase.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/com.luk.timetable2_6.0.4_28.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/com.luk.timetable2_6.0.4_28.apk > com.luk.timetable2_6.0.4_28.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/com.poupa.vinylmusicplayer_0.20.1.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/com.poupa.vinylmusicplayer_0.20.1.apk > com.poupa.vinylmusicplayer_0.20.1.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/de.k3b.android.contentproviderhelper.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/de.k3b.android.contentproviderhelper.apk > de.k3b.android.contentproviderhelper.log 2>&1

echo "analyzing benchmarks/diskDroidBenchmarks/group1/hashengineering.groestlcoin.wallet_71107.apk"
./runSingle.py benchmarks/diskDroidBenchmarks/group1/hashengineering.groestlcoin.wallet_71107.apk > hashengineering.groestlcoin.wallet_71107.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/nightlock-peppercarrot.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/nightlock-peppercarrot.apk > nightlock-peppercarrot.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/org.secuso.privacyfriendlyactivitytracker_1.0.5.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/org.secuso.privacyfriendlyactivitytracker_1.0.5.apk > org.secuso.privacyfriendlyactivitytracker_1.0.5.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/rodrigodavy.com.github.pixelartist.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/rodrigodavy.com.github.pixelartist.apk > rodrigodavy.com.github.pixelartist.log 2>&1

## not sure.
#echo "analyzing benchmarks/diskDroidBenchmarks/group1/bus.chio.wishmaster_1002.apk"
#./runSingle.py benchmarks/diskDroidBenchmarks/group1/bus.chio.wishmaster_1002.apk > bus.chio.wishmaster_1002.log 2>&1

###########################################################################################################################################
# Section 2: apps that could successfully analyzed by fine-grained aggressive analysis by us.
# diskdroid-group1

echo "analyzing benchmarks/diskDroidBenchmarks/group1/com.alfray.timeriffic_10905.apk"
./runSingle.py benchmarks/diskDroidBenchmarks/group1/com.alfray.timeriffic_10905.apk > com.alfray.timeriffic_10905.log 2>&1

echo "analyzing benchmarks/diskDroidBenchmarks/group1/org.fdroid.fdroid_1008000.apk"
./runSingle.py benchmarks/diskDroidBenchmarks/group1/org.fdroid.fdroid_1008000.apk > org.fdroid.fdroid_1008000.log 2>&1

echo "analyzing benchmarks/diskDroidBenchmarks/group1/org.gateshipone.odyssey_30.apk"
./runSingle.py benchmarks/diskDroidBenchmarks/group1/org.gateshipone.odyssey_30.apk > org.gateshipone.odyssey_30.log 2>&1

echo "analyzing benchmarks/diskDroidBenchmarks/group1/org.lumicall.android_190.apk"
./runSingle.py benchmarks/diskDroidBenchmarks/group1/org.lumicall.android_190.apk > org.lumicall.android_190.log 2>&1

# diskdroid-group2
echo "analyzing benchmarks/diskDroidBenchmarks/group2/com.kanedias.vanilla.metadata_5.apk"
./runSingle.py benchmarks/diskDroidBenchmarks/group2/com.kanedias.vanilla.metadata_5.apk > com.kanedias.vanilla.metadata_5.log 2>&1

echo "analyzing benchmarks/diskDroidBenchmarks/group2/org.secuso.privacyfriendlyweather_6.apk"
./runSingle.py benchmarks/diskDroidBenchmarks/group2/org.secuso.privacyfriendlyweather_6.apk > org.secuso.privacyfriendlyweather_6.log 2>&1

# diskdroid-group3
echo "analyzing benchmarks/diskDroidBenchmarks/group3/com.genonbeta.TrebleShot_98.apk"
./runSingle.py benchmarks/diskDroidBenchmarks/group3/com.genonbeta.TrebleShot_98.apk > com.genonbeta.TrebleShot_98.log 2>&1

echo "analyzing benchmarks/diskDroidBenchmarks/group3/com.github.axet.callrecorder_219.apk"
./runSingle.py benchmarks/diskDroidBenchmarks/group3/com.github.axet.callrecorder_219.apk > com.github.axet.callrecorder_219.log 2>&1

echo "analyzing benchmarks/diskDroidBenchmarks/group3/com.zeapo.pwdstore_10303.apk"
./runSingle.py benchmarks/diskDroidBenchmarks/group3/com.zeapo.pwdstore_10303.apk > com.zeapo.pwdstore_10303.log 2>&1

# sparsedroid-opensourceapps
echo "analyzing benchmarks/sparsedroidBenchmark/acr.browser.lightning_4.5.1.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/acr.browser.lightning_4.5.1.apk > acr.browser.lightning_4.5.1.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/com.app.Zensuren_1.21.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/com.app.Zensuren_1.21.apk > com.app.Zensuren_1.21.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/com.github.axet.callrecorder_1.6.44.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/com.github.axet.callrecorder_1.6.44.apk > com.github.axet.callrecorder_1.6.44.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/com.github.yeriomin.dumbphoneassistant_5.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/com.github.yeriomin.dumbphoneassistant_5.apk > com.github.yeriomin.dumbphoneassistant_5.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/com.igisw.openmoneybox.3.4.1.8.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/com.igisw.openmoneybox.3.4.1.8.apk > com.igisw.openmoneybox.3.4.1.8.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/com.ilm.sandwich_2.2.4f.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/com.ilm.sandwich_2.2.4f.apk > com.ilm.sandwich_2.2.4f.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/com.kunzisoft.keepass.libre_2.5.0.0beta18.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/com.kunzisoft.keepass.libre_2.5.0.0beta18.apk > com.kunzisoft.keepass.libre_2.5.0.0beta18.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/com.vonglasow.michael.satstat.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/com.vonglasow.michael.satstat.apk > com.vonglasow.michael.satstat.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/dk.jens.backup_0.3.4.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/dk.jens.backup_0.3.4.apk > dk.jens.backup_0.3.4.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/name.myigel.fahrplan.eh17_1.33.16.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/name.myigel.fahrplan.eh17_1.33.16.apk > name.myigel.fahrplan.eh17_1.33.16.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/net.ddns.mlsoftlaberge.trycorder.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/net.ddns.mlsoftlaberge.trycorder.apk > net.ddns.mlsoftlaberge.trycorder.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/nya.miku.wishmaster.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/nya.miku.wishmaster.apk > nya.miku.wishmaster.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/opencontacts.open.com.opencontacts_12.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/opencontacts.open.com.opencontacts_12.apk > opencontacts.open.com.opencontacts_12.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/org.csploit.android.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/org.csploit.android.apk > org.csploit.android.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/org.decsync.sparss.floss_1.13.4.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/org.decsync.sparss.floss_1.13.4.apk > org.decsync.sparss.floss_1.13.4.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/org.gateshipone.odyssey_1.1.17.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/org.gateshipone.odyssey_1.1.17.apk > org.gateshipone.odyssey_1.1.17.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/org.materialos.icons_2.1.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/org.materialos.icons_2.1.apk > org.materialos.icons_2.1.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/org.secuso.privacyfriendlytodolist_2.1.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/org.secuso.privacyfriendlytodolist_2.1.apk > org.secuso.privacyfriendlytodolist_2.1.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/org.totschnig.myexpenses.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/org.totschnig.myexpenses.apk > org.totschnig.myexpenses.log 2>&1

# sparsedroid-realworldapps
echo "analyzing benchmarks/sparsedroidBenchmark/com.adobe.reader_19.2.1.9183.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/com.adobe.reader_19.2.1.9183.apk > com.adobe.reader_19.2.1.9183.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/com.microsoft.office.word_16.0.11425.20132.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/com.microsoft.office.word_16.0.11425.20132.apk > com.microsoft.office.word_16.0.11425.20132.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/com.emn8.mobilem8.nativeapp.bk_5.0.10.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/com.emn8.mobilem8.nativeapp.bk_5.0.10.apk > com.emn8.mobilem8.nativeapp.bk_5.0.10.log 2>&1

########################################################################################################################################
# Section 3: apps which either run out of memory or could not be analyzed within the given budget. Should be consided in the future.
echo "analyzing benchmarks/diskDroidBenchmarks/group2/com.github.axet.bookreader_375.apk"
./runSingle.py benchmarks/diskDroidBenchmarks/group2/com.github.axet.bookreader_375.apk > com.github.axet.bookreader_375.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/com.ichi2.anki_2.8.4.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/com.ichi2.anki_2.8.4.apk > com.ichi2.anki_2.8.4.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/com.microsoft.office.outlook_3.0.46.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/com.microsoft.office.outlook_3.0.46.apk > com.microsoft.office.outlook_3.0.46.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/com.nianticlabs.pokemongo_0.139.3.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/com.nianticlabs.pokemongo_0.139.3.apk > com.nianticlabs.pokemongo_0.139.3.log 2>&1

echo "analyzing benchmarks/diskDroidBenchmarks/group3/de.k3b.android.androFotoFinder_44.apk"
./runSingle.py benchmarks/diskDroidBenchmarks/group3/de.k3b.android.androFotoFinder_44.apk > de.k3b.android.androFotoFinder_44.log 2>&1

echo "analyzing benchmarks/diskDroidBenchmarks/group1/F-Droid.apk"
./runSingle.py benchmarks/diskDroidBenchmarks/group1/F-Droid.apk > F-Droid.log 2>&1

echo "analyzing benchmarks/diskDroidBenchmarks/group1/nya.miku.wishmaster_54.apk"
./runSingle.py benchmarks/diskDroidBenchmarks/group1/nya.miku.wishmaster_54.apk > nya.miku.wishmaster_54.log 2>&1

echo "analyzing benchmarks/sparsedroidBenchmark/org.openpetfoodfacts.scanner_2.9.8.apk"
./runSingle.py benchmarks/sparsedroidBenchmark/org.openpetfoodfacts.scanner_2.9.8.apk > org.openpetfoodfacts.scanner_2.9.8.log 2>&1

##########################