# ใบความรู้ที่ 6 — หน่วยที่ 6

| | | |
| --- | --- | --- |
| **ใบความรู้ที่ 6** | **รหัสวิชา 31909-1001 วิชา ระบบปฏิบัติการ** | **หน่วยที่ 6** |
| **ชื่อหน่วยการเรียนรู้:** การจัดการระบบแฟ้ม | **สอนครั้งที่ 10** | **ทฤษฎี 2 ชม. / ปฏิบัติ 3 ชม.** |

**ชื่อเรื่อง:** การจัดการระบบแฟ้มในระบบปฏิบัติการ Linux

---

## 1. ผลลัพธ์การเรียนรู้ระดับหน่วยการเรียน

ผู้เรียนสามารถอธิบายแนวคิดของระบบแฟ้ม โครงสร้างไดเรกทอรี ประเภทของระบบแฟ้มที่ใช้ใน Linux การจัดการสิทธิ์การเข้าถึง การแบ่งพาร์ทิชัน การ mount และการสำรองข้อมูล พร้อมทั้งสามารถปฏิบัติการจัดการระบบแฟ้มบน Linux ได้อย่างถูกต้อง ปลอดภัย รอบคอบ และเป็นระเบียบ

## 2. อ้างอิงมาตรฐาน/เชื่อมโยงกลุ่มอาชีพ

มาตรฐานอาชีพ: มาตรฐานฝีมือแรงงานแห่งชาติ กรมพัฒนาฝีมือแรงงาน อาชีพช่างซ่อมไมโครคอมพิวเตอร์ ระดับ 2 เชื่อมโยง กลุ่มอาชีพฮาร์ดแวร์ สาขาวิชาเทคโนโลยีคอมพิวเตอร์ สมรรถนะย่อย 02.5 ปรับแต่งระบบแฟ้มและสิทธิ์

## 3. สมรรถนะประจำหน่วย

3.1 ประมวลความรู้เกี่ยวกับแนวคิด โครงสร้าง และประเภทของระบบแฟ้มใน Linux

3.2 ปรับแต่งระบบแฟ้ม การแบ่งพาร์ทิชัน และสิทธิ์การเข้าถึงตามที่กำหนด

## 4. จุดประสงค์เชิงพฤติกรรม

4.1 อธิบายแนวคิดและคุณสมบัติของแฟ้มและระบบแฟ้มได้ถูกต้อง

4.2 เปรียบเทียบระบบแฟ้ม ext4, XFS, Btrfs, FAT32, exFAT, NTFS ได้

4.3 อธิบายโครงสร้าง inode, directory และ Linux Filesystem Hierarchy Standard (FHS) ได้

4.4 จัดการสิทธิ์การเข้าถึงด้วย chmod, chown, ACL ได้อย่างถูกต้อง

4.5 แบ่งพาร์ทิชัน ฟอร์แมต mount และสำรองข้อมูลบน Linux ได้

---

## 5. เนื้อหาสาระ

### 5.1 แนวคิดและคุณสมบัติของแฟ้ม (File Concept)

แฟ้ม (File) คือ ชุดข้อมูลที่ถูกตั้งชื่อและจัดเก็บไว้ในหน่วยความจำสำรอง (Secondary Storage) เพื่อให้ระบบปฏิบัติการและผู้ใช้สามารถเรียกใช้ได้ในภายหลัง ระบบแฟ้ม (File System) คือ วิธีการที่ระบบปฏิบัติการใช้ในการจัดระเบียบ จัดเก็บ ค้นหา และควบคุมการเข้าถึงข้อมูลบนอุปกรณ์เก็บข้อมูล

**คุณสมบัติของแฟ้ม (File Attributes):**

- **Name** — ชื่อแฟ้มในรูปแบบที่มนุษย์อ่านได้
- **Type** — ประเภทของแฟ้ม (regular, directory, symbolic link, device ฯลฯ)
- **Size** — ขนาดของแฟ้มเป็นไบต์
- **Location** — ตำแหน่งข้อมูลจริงบนอุปกรณ์ (ชี้ผ่าน inode)
- **Protection / Permissions** — สิทธิ์การเข้าถึง (read, write, execute)
- **Owner / Group** — เจ้าของและกลุ่ม
- **Timestamps** — เวลาสร้าง (ctime), แก้ไข (mtime), เข้าถึง (atime)

**การปฏิบัติการพื้นฐานกับแฟ้ม (File Operations):** create, open, read, write, append, seek, close, delete, truncate, rename

**ประเภทของแฟ้มใน Linux (แสดงด้วยอักษรตัวแรกของ `ls -l`):**

| สัญลักษณ์ | ประเภท | ตัวอย่าง |
| --- | --- | --- |
| `-` | Regular file | ไฟล์ข้อมูล เอกสาร โปรแกรม |
| `d` | Directory | โฟลเดอร์ |
| `l` | Symbolic link | ลิงก์ชี้ไปยังไฟล์อื่น |
| `c` | Character device | `/dev/tty`, `/dev/null` |
| `b` | Block device | `/dev/sda`, `/dev/nvme0n1` |
| `p` | Named pipe (FIFO) | ท่อส่งข้อมูลระหว่างโพรเซส |
| `s` | Socket | จุดสื่อสารระหว่างโพรเซส |

```bash
ls -l /dev | head
file /etc/passwd          # ตรวจสอบประเภทของไฟล์
stat /etc/passwd          # ดู attributes ครบถ้วน รวม inode
```

### 5.2 โครงสร้างไดเรกทอรี (Directory Structure)

โครงสร้างไดเรกทอรีเป็นวิธีการจัดระเบียบแฟ้มเชิงตรรกะ ระบบปฏิบัติการมีวิวัฒนาการของโครงสร้างไดเรกทอรีดังนี้

- **Single-level** — ทุกไฟล์อยู่ในไดเรกทอรีเดียว ง่ายแต่ชื่อชนกันง่าย
- **Two-level** — แยกไดเรกทอรีต่อผู้ใช้
- **Tree-structured** — โครงสร้างต้นไม้ (Linux ใช้แบบนี้) มี root `/` เป็นราก
- **Acyclic Graph** — รองรับการแชร์ไฟล์ผ่าน link (hard/symbolic link)
- **General Graph** — อนุญาตให้มี cycle (ต้องมีกลไกป้องกัน loop)

### 5.3 Linux Filesystem Hierarchy Standard (FHS)

Linux จัดระเบียบไดเรกทอรีตามมาตรฐาน FHS โดยเริ่มจาก root `/` ดังนี้

| ไดเรกทอรี | หน้าที่ |
| --- | --- |
| `/` | รากของระบบแฟ้มทั้งหมด |
| `/bin` | คำสั่งพื้นฐานสำหรับผู้ใช้ทุกคน (ls, cp, mv) |
| `/sbin` | คำสั่งสำหรับผู้ดูแลระบบ (fdisk, mkfs) |
| `/etc` | ไฟล์ตั้งค่าระบบ |
| `/home` | ไดเรกทอรีบ้านของผู้ใช้ |
| `/root` | ไดเรกทอรีบ้านของ root |
| `/var` | ข้อมูลที่เปลี่ยนแปลง เช่น log, cache, mail |
| `/tmp` | ไฟล์ชั่วคราว |
| `/usr` | โปรแกรมและไลบรารีของผู้ใช้ |
| `/lib` | ไลบรารีที่จำเป็นและ Kernel Module |
| `/dev` | Device node |
| `/proc` | ข้อมูล runtime ของ Kernel และโพรเซส |
| `/sys` | ข้อมูล Kernel object และอุปกรณ์ |
| `/mnt` | จุด mount ชั่วคราวสำหรับผู้ดูแลระบบ |
| `/media` | จุด mount อัตโนมัติของสื่อ removable |
| `/boot` | Kernel และ Bootloader (GRUB) |
| `/opt` | ซอฟต์แวร์เสริมจากผู้ผลิตอื่น |

```bash
man hier          # ดูคำอธิบายมาตรฐาน FHS
ls /
tree -L 1 /       # แสดงโครงสร้างไดเรกทอรีระดับ 1
```

### 5.4 inode และการจัดเก็บข้อมูลใน Linux

Linux ใช้แนวคิด **inode (Index Node)** ในการเก็บ metadata ของแต่ละไฟล์ โดย inode หนึ่งตัวเก็บข้อมูลทุกอย่างของไฟล์ **ยกเว้นชื่อไฟล์** (ชื่อไฟล์ถูกเก็บใน directory entry ที่ชี้ไปยัง inode number)

**ข้อมูลที่เก็บใน inode:**

- inode number
- ประเภทและสิทธิ์ (mode)
- Owner (UID) และ Group (GID)
- ขนาดไฟล์
- Timestamps (atime, mtime, ctime)
- Link count (จำนวน hard link)
- Pointer ชี้ไปยัง data block บนดิสก์ (direct, single/double/triple indirect)

``` 
Directory Entry            inode Table              Data Blocks
┌──────────────┐          ┌────────────────┐       ┌──────────┐
│ name: doc.txt│──────────▶│ inode #12345   │──────▶│ block 100│
│ inode: 12345 │          │ mode, uid, gid │──────▶│ block 101│
└──────────────┘          │ size, times    │──────▶│ block 102│
                          │ block pointers │       └──────────┘
                          └────────────────┘
```

```bash
ls -i doc.txt          # ดู inode number
df -i                  # ดูจำนวน inode ที่ใช้/เหลือของแต่ละ filesystem
stat doc.txt           # ดูรายละเอียด inode
```

**Hard Link vs Symbolic Link:**

- **Hard link** — directory entry อีกอันที่ชี้ inode เดียวกัน ใช้พื้นที่เดียวกัน ลบต้นฉบับแล้วข้อมูลยังอยู่ (ใช้ `ln source link`) ข้ามพาร์ทิชันไม่ได้
- **Symbolic (soft) link** — ไฟล์พิเศษที่เก็บ path ชี้ไปไฟล์อื่น ข้ามพาร์ทิชันได้ ลบต้นฉบับแล้วลิงก์เสีย (ใช้ `ln -s source link`)

```bash
ln file.txt hardlink.txt      # hard link
ln -s file.txt softlink.txt   # symbolic link
ls -li file.txt hardlink.txt softlink.txt
```

### 5.5 ประเภทของระบบแฟ้มใน Linux และระบบอื่น

| ระบบแฟ้ม | ใช้กับ OS | Journaling | ขนาดไฟล์สูงสุด | จุดเด่น |
|---|---|---|---|---|
| **ext4** | Linux | ✔ | 16 TB | มาตรฐาน Linux เสถียร รองรับ extent |
| **XFS** | Linux | ✔ | 8 EB | ประสิทธิภาพสูงกับไฟล์ใหญ่ ขยายได้ |
| **Btrfs** | Linux | ✔ (CoW) | 16 EB | Snapshot, Subvolume, Checksum, RAID |
| **ZFS** | Linux/BSD | ✔ (CoW) | 16 EB | Data integrity, Snapshot, Pool |
| **FAT32** | ทุก OS | ✘ | 4 GB | เข้ากันได้ทุกระบบ แต่ไฟล์ ≤ 4 GB |
| **exFAT** | ทุก OS | ✘ | 16 EB | รองรับไฟล์ใหญ่ เหมาะกับ Flash |
| **NTFS** | Windows/Linux(ntfs-3g) | ✔ | 16 EB | ระบบไฟล์หลักของ Windows |

**Journaling** คือ กลไกที่บันทึกการเปลี่ยนแปลงลง Journal ก่อนเขียนจริง เพื่อป้องกันข้อมูลเสียหายเมื่อไฟดับ/ระบบล่ม ทำให้ฟื้นตัวเร็ว **Copy-on-Write (CoW)** ของ Btrfs/ZFS ไม่เขียนทับข้อมูลเดิม แต่เขียนสำเนาใหม่แล้วปรับ pointer ทำให้ Snapshot มีประสิทธิภาพ

```bash
cat /proc/filesystems      # ระบบแฟ้มที่ Kernel รองรับ
lsblk -f                   # ดู FS Type ของแต่ละพาร์ทิชัน
df -Th                     # ดู FS Type และพื้นที่
```

### 5.6 การแบ่งพาร์ทิชัน (Partitioning)

**MBR (Master Boot Record) vs GPT (GUID Partition Table):**

| รายการ | MBR | GPT |
|---|---|---|
| ขนาดดิสก์สูงสุด | 2 TB | 9.4 ZB |
| จำนวนพาร์ทิชัน | 4 Primary | 128 (ค่าเริ่มต้น) |
| Boot mode | Legacy BIOS | UEFI |
| สำรอง Partition Table | ไม่มี | มี (ต้นและท้ายดิสก์) |

**เครื่องมือแบ่งพาร์ทิชันบน Linux:**

```bash
sudo lsblk                          # ดูโครงสร้างดิสก์
sudo fdisk /dev/sdX                 # แบ่งพาร์ทิชันแบบ MBR (interactive)
sudo gdisk /dev/sdX                 # แบ่งพาร์ทิชันแบบ GPT
sudo parted /dev/sdX                # เครื่องมือครบวงจร (MBR/GPT)
sudo cfdisk /dev/sdX                # แบบ TUI ใช้ง่าย
```

ตัวอย่างการใช้ parted สร้าง GPT และพาร์ทิชันเดียว:

```bash
sudo parted /dev/sdX mklabel gpt
sudo parted -a optimal /dev/sdX mkpart primary ext4 0% 100%
sudo partprobe /dev/sdX
```

### 5.7 การฟอร์แมตและสร้างระบบแฟ้ม (mkfs)

```bash
sudo mkfs.ext4 /dev/sdX1                 # ฟอร์แมตเป็น ext4
sudo mkfs.ext4 -L DATA /dev/sdX1         # กำหนด Label = DATA
sudo mkfs.xfs /dev/sdX1                   # ฟอร์แมตเป็น XFS
sudo mkfs.vfat -F 32 /dev/sdX1            # ฟอร์แมตเป็น FAT32
sudo mkfs.exfat /dev/sdX1                 # ฟอร์แมตเป็น exFAT
sudo mkfs.ntfs -Q /dev/sdX1              # ฟอร์แมตเป็น NTFS (quick)
```

**ตรวจสอบและซ่อมระบบแฟ้ม:**

```bash
sudo fsck /dev/sdX1              # ตรวจและซ่อม (ต้อง unmount ก่อน)
sudo e2fsck -f /dev/sdX1        # บังคับตรวจ ext2/3/4
sudo xfs_repair /dev/sdX1       # ซ่อม XFS
sudo tune2fs -l /dev/sdX1       # ดูข้อมูล superblock ของ ext4
```

### 5.8 การ Mount และ Unmount

```bash
sudo mkdir -p /mnt/data
sudo mount /dev/sdX1 /mnt/data                    # mount พื้นฐาน
sudo mount -o ro,noexec,nosuid /dev/sdX1 /mnt/data  # mount แบบจำกัดสิทธิ์
mount | grep sdX1                                  # ตรวจสอบ
findmnt /mnt/data                                  # แสดงเป็น tree
sudo umount /mnt/data                              # unmount
```

**Mount option ที่ควรรู้จัก:** `ro` (read-only), `rw` (read-write), `noexec` (ห้ามรันไฟล์), `nosuid` (ปิด setuid), `noatime` (ไม่อัปเดตเวลาเข้าถึง เพิ่มประสิทธิภาพ), `nofail` (บูตต่อได้แม้ mount ไม่ได้), `defaults`

**Mount อัตโนมัติเมื่อบูตด้วย /etc/fstab:**

```bash
$ sudo blkid /dev/sdX1     # หา UUID และ TYPE
# เพิ่มบรรทัดใน /etc/fstab:
# UUID=xxxx-xxxx  /mnt/data  ext4  defaults,noatime,nofail  0  2
$ sudo mount -a            # ทดสอบโดยไม่รีบูต
```

โครงสร้างของแต่ละบรรทัดใน /etc/fstab มี 6 ฟิลด์: `<device> <mount point> <fstype> <options> <dump> <pass>`

### 5.9 การจัดการสิทธิ์การเข้าถึง (File Permissions)

Linux กำหนดสิทธิ์แยกเป็น 3 กลุ่ม: **owner (u), group (g), others (o)** แต่ละกลุ่มมีสิทธิ์ **read (r=4), write (w=2), execute (x=1)**

```
-rwxr-xr--  1 user group  4096 Jul 16 10:00 script.sh
│└┬┘└┬┘└┬┘
│ │  │  └── others: r--  (4)
│ │  └───── group : r-x  (5)
│ └──────── owner : rwx  (7)
└────────── type  : regular file
```

**เปลี่ยนสิทธิ์ด้วย chmod:**

```bash
chmod 755 script.sh          # rwxr-xr-x (โหมดตัวเลข)
chmod u+x script.sh          # เพิ่ม execute ให้ owner (สัญลักษณ์)
chmod go-w file.txt          # ถอด write จาก group และ others
chmod -R 750 /mnt/data/dir   # เปลี่ยนแบบ recursive
```

**เปลี่ยนเจ้าของด้วย chown / chgrp:**

```bash
sudo chown user file.txt              # เปลี่ยน owner
sudo chown user:group file.txt        # เปลี่ยน owner และ group
sudo chgrp group file.txt             # เปลี่ยนเฉพาะ group
sudo chown -R user:group /mnt/data    # recursive
```

**Special Permissions:**

- **SUID (4xxx)** — รันด้วยสิทธิ์ของเจ้าของไฟล์ เช่น `/usr/bin/passwd`
- **SGID (2xxx)** — รันด้วยสิทธิ์ของ group หรือไฟล์ใหม่ในไดเรกทอรีสืบทอด group
- **Sticky bit (1xxx)** — ลบไฟล์ได้เฉพาะเจ้าของ เช่น `/tmp`

```bash
chmod 4755 program      # ตั้ง SUID
chmod 2755 shared_dir   # ตั้ง SGID
chmod 1777 /tmp         # ตั้ง Sticky bit
ls -ld /tmp             # จะเห็น drwxrwxrwt
```

### 5.10 Access Control List (ACL)

เมื่อสิทธิ์แบบ owner/group/other ไม่พอ Linux รองรับ ACL เพื่อกำหนดสิทธิ์ให้ผู้ใช้/กลุ่มเฉพาะราย

```bash
getfacl file.txt                       # ดู ACL
setfacl -m u:alice:rw file.txt         # ให้ alice อ่าน-เขียน
setfacl -m g:dev:r-- file.txt          # ให้กลุ่ม dev อ่านอย่างเดียว
setfacl -x u:alice file.txt            # ลบ ACL ของ alice
setfacl -b file.txt                    # ลบ ACL ทั้งหมด
```

> หมายเหตุ: ไฟล์ที่มี ACL จะแสดงเครื่องหมาย `+` ท้ายสิทธิ์เมื่อใช้ `ls -l` เช่น `-rw-rw-r--+`

### 5.11 การสำรองและกู้คืนข้อมูล (Backup & Restore)

```bash
# tar — สำรองเป็นไฟล์บีบอัด
$ tar -czvf backup.tar.gz /home/user/docs
$ tar -xzvf backup.tar.gz -C /restore/path

# rsync — คัดลอกแบบ incremental (เร็ว เหมาะทำ backup ประจำ)
$ rsync -avh --delete /source/ /backup/
$ rsync -avz /source/ user@server:/backup/   # ผ่านเครือข่าย

# dd — clone ทั้งพาร์ทิชัน/ดิสก์ (ระวังมาก)
$ sudo dd if=/dev/sdX of=/backup/disk.img bs=4M status=progress

# cp -a — คัดลอกโดยรักษาสิทธิ์และ timestamp
$ cp -a /source /dest
```

**เครื่องมือสำรองข้อมูลระดับสูง:** `timeshift` (snapshot ระบบ), `borgbackup` / `restic` (deduplication + encryption), Btrfs/ZFS snapshot

### 5.12 การตรวจสอบและจัดการพื้นที่ดิสก์

```bash
df -Th                        # พื้นที่ว่างของแต่ละ filesystem
du -sh /var/log               # ขนาดรวมของไดเรกทอรี
du -h --max-depth=1 /home | sort -h   # ไดเรกทอรีย่อยเรียงตามขนาด
ncdu /                        # เครื่องมือดูการใช้พื้นที่แบบ interactive
lsblk -o NAME,SIZE,FSUSE%,MOUNTPOINT
```

### 5.13 การขยาย/ลดขนาดระบบแฟ้ม (Resize)

```bash
# ขยาย ext4 (ต้องขยายพาร์ทิชันก่อน)
$ sudo resize2fs /dev/sdX1

# ขยาย XFS (ขยายได้อย่างเดียว ลดไม่ได้)
$ sudo xfs_growfs /mnt/data

# ผ่าน LVM (Logical Volume Manager)
$ sudo lvextend -L +5G /dev/vg0/lv_data
$ sudo resize2fs /dev/vg0/lv_data
```

---

## 6. แบบฝึกหัด/แบบทดสอบ

**คำชี้แจง:** ให้ผู้เรียนตอบคำถามต่อไปนี้ลงในกระดาษคำตอบ พร้อมแสดงคำสั่งหรือตัวอย่างประกอบ (ถ้ามี)

1. อธิบายความหมายของแฟ้มและระบบแฟ้ม พร้อมยกตัวอย่างคุณสมบัติของแฟ้มอย่างน้อย 5 ข้อ
2. อธิบายประเภทของแฟ้มใน Linux ที่แสดงด้วยอักษรตัวแรกใน `ls -l` ครบทุกชนิด
3. inode คืออะไร เก็บข้อมูลอะไรบ้าง และเหตุใดจึงไม่เก็บชื่อไฟล์ไว้ใน inode
4. อธิบายความแตกต่างระหว่าง Hard link กับ Symbolic link พร้อมข้อจำกัดของแต่ละแบบ
5. เปรียบเทียบระบบแฟ้ม ext4, XFS และ Btrfs ในแง่ Journaling, ขนาดไฟล์สูงสุด และจุดเด่น
6. เปรียบเทียบ FAT32, exFAT และ NTFS พร้อมระบุสถานการณ์ที่ควรเลือกใช้แต่ละแบบ
7. เปรียบเทียบ MBR กับ GPT ในแง่ขนาดดิสก์สูงสุด จำนวนพาร์ทิชัน และ Boot mode
8. เขียนคำสั่งฟอร์แมตพาร์ทิชัน /dev/sdb1 เป็น ext4 พร้อมกำหนด Label = DATA
9. อธิบายความหมายและประโยชน์ของ Journaling พร้อมยกตัวอย่างสถานการณ์ที่ช่วยป้องกันข้อมูลเสียหาย
10. อธิบายความหมายของแต่ละฟิลด์ในบรรทัดของ /etc/fstab ทั้ง 6 ฟิลด์
11. เขียนคำสั่ง mount พาร์ทิชัน /dev/sdb1 ที่ /mnt/data แบบ read-only และห้ามรันไฟล์
12. `chmod 750 file` ให้สิทธิ์อะไรกับ owner, group และ others
13. เขียนคำสั่งเปลี่ยนเจ้าของไฟล์ report.txt ให้เป็น user=alice group=dev แบบ recursive
14. อธิบายความหมายของ SUID, SGID และ Sticky bit พร้อมยกตัวอย่างไฟล์/ไดเรกทอรีที่ใช้จริง
15. ใช้คำสั่ง setfacl อย่างไรเพื่อให้ผู้ใช้ bob มีสิทธิ์อ่าน-เขียนไฟล์ data.txt โดยไม่กระทบสิทธิ์เดิม
16. เปรียบเทียบการใช้ tar, rsync และ dd ในการสำรองข้อมูล พร้อมระบุสถานการณ์ที่เหมาะสม
17. เขียนคำสั่งดูพื้นที่ว่างของทุก filesystem และคำสั่งดูขนาดรวมของไดเรกทอรี /var/log
18. เขียนคำสั่งขยายระบบแฟ้ม ext4 บนพาร์ทิชัน /dev/sda1 หลังขยายพาร์ทิชันแล้ว
19. อธิบายมาตรฐาน FHS พร้อมระบุหน้าที่ของ /etc, /var, /home, /boot และ /proc
20. **Case Study:** ลูกค้าต้องการ Flash drive ที่ใช้ได้ทั้ง Windows, macOS และ Linux และต้องเก็บไฟล์วิดีโอขนาด 8 GB ควรเลือกระบบแฟ้มใด เพราะอะไร และเขียนคำสั่งฟอร์แมตบน Linux

---

## 7. เอกสารอ้างอิง

1. Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). *Operating System Concepts* (10th ed.). Wiley. Chapter 13–15: File-System.
2. Tanenbaum, A. S., & Bos, H. (2014). *Modern Operating Systems* (4th ed.). Pearson. Chapter 4: File Systems.
3. Nemeth, E., et al. (2017). *UNIX and Linux System Administration Handbook* (5th ed.). Addison-Wesley.
4. Filesystem Hierarchy Standard (FHS) 3.0: <https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html>
5. Linux man pages: `ls(1)`, `stat(1)`, `chmod(1)`, `chown(1)`, `setfacl(1)`, `mount(8)`, `fstab(5)`, `mkfs(8)`, `fsck(8)`, `tar(1)`, `rsync(1)`
6. ext4 Documentation: <https://www.kernel.org/doc/html/latest/filesystems/ext4/>
7. Btrfs Wiki: <https://btrfs.readthedocs.io/>
8. Ubuntu Server Guide. <https://ubuntu.com/server/docs>
9. Red Hat Enterprise Linux Storage Administration Guide.

---

## 8. ภาคผนวก

### ภาคผนวก ก: สรุปคำสั่งจัดการระบบแฟ้มบน Linux

| คำสั่ง | วัตถุประสงค์ |
|---|---|
| `ls -li` | แสดงไฟล์พร้อม inode number |
| `stat FILE` | ดู metadata ของไฟล์ |
| `df -Th` | พื้นที่ว่างและ FS Type |
| `du -sh DIR` | ขนาดรวมของไดเรกทอรี |
| `lsblk -f` | โครงสร้างดิสก์พร้อม FS/UUID |
| `blkid` | ดู UUID และ TYPE |
| `fdisk / gdisk / parted` | แบ่งพาร์ทิชัน |
| `mkfs.ext4 / mkfs.vfat / mkfs.exfat` | สร้างระบบแฟ้ม |
| `fsck / e2fsck / xfs_repair` | ตรวจและซ่อมระบบแฟ้ม |
| `mount / umount / findmnt` | แนบ/ถอน filesystem |
| `chmod / chown / chgrp` | จัดการสิทธิ์และเจ้าของ |
| `getfacl / setfacl` | จัดการ ACL |
| `tar / rsync / dd` | สำรองและกู้คืนข้อมูล |
| `resize2fs / xfs_growfs` | ขยายระบบแฟ้ม |
| `tune2fs -l` | ดูข้อมูล superblock |

### ภาคผนวก ข: ตารางสิทธิ์แบบตัวเลข (Octal Permission)

| ตัวเลข | สิทธิ์ | ความหมาย |
|---|---|---|
| 7 | rwx | อ่าน เขียน รัน |
| 6 | rw- | อ่าน เขียน |
| 5 | r-x | อ่าน รัน |
| 4 | r-- | อ่านอย่างเดียว |
| 3 | -wx | เขียน รัน |
| 2 | -w- | เขียนอย่างเดียว |
| 1 | --x | รันอย่างเดียว |
| 0 | --- | ไม่มีสิทธิ์ |

**ตัวอย่างที่พบบ่อย:** `644` (ไฟล์ทั่วไป), `755` (โปรแกรม/ไดเรกทอรี), `600` (ไฟล์ลับ เช่น key), `700` (ไดเรกทอรีส่วนตัว), `777` (ทุกคนทำได้ทุกอย่าง — ควรหลีกเลี่ยง)

---
