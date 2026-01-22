# Troubleshooting Network Connectivity

This guide helps diagnose common connection issues when connecting to IBM i systems.

## Problem: Connection Timeout

### Symptoms
```
Execution Error: Connection failed: timed out
```
or
```
[WinError 10060] Se produjo un error durante el intento de conexión...
```

### Diagnosis Steps

#### 1. Verify Network Connectivity (Ping)
```powershell
ping 192.168.1.3
```

**Expected Output:**
- ✅ Success: `Reply from 192.168.1.3: bytes=32 time=Xms`
- ❌ Failure: `Request timed out` → Check VPN/Network

#### 2. Test SSH Port Access
```powershell
Test-NetConnection -ComputerName 192.168.1.3 -Port 22
```

**Expected Output:**
- ✅ Success: `TcpTestSucceeded : True`
- ❌ Failure: `TcpTestSucceeded : False` → Firewall blocking SSH

### Common Solutions

#### Firewall Blocking Port 22
**Cause:** Corporate firewall or IBM i host firewall blocking SSH traffic.

**Solution:**
1. Contact your network administrator
2. Request access from your IP to IBM i on port 22
3. Verify SSH service is running on IBM i: `STRTCPSVR SERVER(*SSHD)`

#### Wrong SSH Port
**Cause:** SSH might be running on a non-standard port (e.g., 2222).

**Solution:**
1. Ask your IBM i administrator for the correct SSH port
2. Update `.env` file:
   ```
   IBMI_PORT=2222
   ```

#### VPN Not Connected
**Cause:** IBM i is on internal network, requires VPN.

**Solution:**
1. Verify VPN connection is active
2. Retry after connecting to VPN

#### SSH Service Not Running
**Cause:** SSHD not started on IBM i.

**Solution (requires IBM i access):**
```
STRTCPSVR SERVER(*SSHD)
```

## Problem: Authentication Failure

### Symptoms
```
Execution Error: Connection failed: Authentication failed
```

### Solutions
1. Verify credentials in `.env`:
   - `IBMI_USER` - Must be a valid IBM i user profile
   - `IBMI_PASS` - Correct password (check for special characters)
2. Check if user profile is disabled: `DSPUSRPRF USRPRF(USERNAME)`
3. Verify password hasn't expired

## Diagnostic Script

Use the included diagnostic tool:
```powershell
uv run scripts/debug_connect.py
```

This will:
- Test SSH connection with verbose logging
- Show exactly where the connection fails
- Suggest specific fixes based on the error
