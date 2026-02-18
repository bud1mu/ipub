# ipub 🌐

**ipub** is a lightweight command-line interface (CLI) tool written in Python to check your public IPv4 or IPv6 address and retrieve geolocation details (ISP, City, Country, Timezone).

The output is strictly **JSON**, making it perfect for parsing in scripts, automation, or logging.

---

## 🚀 Features

* ⚡ **Fast**: Uses `curl` and lightweight Python standard libraries.
* 📡 **Dual Stack**: Support for both `-v4` (IPv4) and `-v6` (IPv6).
* 📍 **Geolocation**: Fetches detailed info via `ip-api.com`.
* 🤖 **Automation Ready**: Outputs clean JSON.
* 🧾 **Clean Terminal Output**: Properly formatted JSON with newline.

---

## 📋 Prerequisites

Make sure the following are installed:

* **Python 3.x**
* **curl**

Check installation:

```bash
python3 --version
curl --version
```

If not installed:

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install python3 curl -y
```

### Arch Linux

```bash
sudo pacman -S python curl
```

### macOS (Homebrew)

```bash
brew install python curl
```

---

# 📦 Installation

Install `ipub` system-wide so it can be used anywhere.

### 1️⃣ Clone the repository

```bash
git clone https://github.com/bud1mu/ipub.git
cd ipub
```

### 2️⃣ Make the script executable

```bash
chmod +x ipub
```

### 3️⃣ Move it to a global binary directory

```bash
sudo mv ipub /usr/local/bin/ipub
```

> `/usr/local/bin` is preferred over `/usr/bin` for manually installed tools.

### 4️⃣ Verify installation

```bash
ipub -v4
```

If it prints JSON output, installation was successful ✅

---

## 🧪 Usage

```bash
ipub -v4   # Prefer IPv4
ipub -v6   # Prefer IPv6
```

---

## 📤 Example Output

```json
{
  "status": "ok",
  "ipv4": "203.0.113.10",
  "ipv6": null,
  "location": {
    "country": "Indonesia",
    "region": "Jakarta",
    "city": "Jakarta",
    "lat": -6.2,
    "lon": 106.8,
    "timezone": "Asia/Jakarta"
  },
  "isp": {
    "isp": "Example ISP",
    "org": "Example Org",
    "as": "AS12345 Example ASN"
  }
}
```




