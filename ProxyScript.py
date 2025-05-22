from Crypto.PublicKey import RSA
from Crypto.Hash import SHA1
from Crypto.Signature import PKCS1_v1_5
import base64
import win32api
import win32con
import win32process
import re
from ctypes import windll
from ctypes.wintypes import *

SCRIPT_PREPEND = """Spawn(function()
    while true do
        Wait(0.1)

        ypcall(function()
            local asset = game:GetObjects("rbxasset://loader.rbxmx")

            -- just to not run the first time
            if _G.gkey == nil then
                _G.gkey = asset[1].Key.Value
            elseif _G.gkey ~= asset[1].Key.Value then
                _G.gkey = asset[1].Key.Value

                local f, e = loadstring(asset[1].Code.Source, "=LocalScript")

                if not f then
                    warn(e)
                else
                    Spawn(f)
                end
            end
        end)
    end
end)"""
PUBLIC_KEY = open("public.bin").read()
PRIVATE_KEY = open("private.pem").read()

key = RSA.import_key(PRIVATE_KEY)
seenPids = {}

def SignScript(script):
    script = re.sub("--rbxsig%.*%\n", "", script)
    script = "\r\n" + script
    final = "--rbxsig%" + base64.b64encode(PKCS1_v1_5.new(key).sign(SHA1.new(script.encode("utf-8")))).decode("utf-8") + "%" + script
    
    return final

count = 0

def response(flow):
    if flow.response.text.find("--rbxsig%") != -1:
        #global count
        
        #count = count + 1

        # patching first one crashes for some reason (Hexagon)
        #if count == 1:
        #    return

        # lol idk python
        for pid in win32process.EnumProcesses():
            try:
                handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, False, pid)

                if handle != 0:
                    path = win32process.GetModuleFileNameEx(handle, 0)

                    win32api.CloseHandle(handle)

                    if path.find("MercuryPlayerBeta") != -1:
                        if pid in seenPids:
                            print("<<<<<<<<< PID already seen, restoring >>>>>>>>>>")
                            handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid)
                            vqex = windll.kernel32.VirtualProtectEx
                            vqex.restype = BOOL
                            vqex.argtypes = [ LONG, LONG, LONG, DWORD, PDWORD ]
                            dw = DWORD(0)
                            vqex(int(handle), seenPids[pid][0], len(PUBLIC_KEY) + 1, 64, PDWORD(dw))
                            win32process.WriteProcessMemory(handle, seenPids[pid][0], seenPids[pid][1])
                            vqex(int(handle), seenPids[pid][0], len(PUBLIC_KEY) + 1, dw, PDWORD(dw))
                        else:
                            print("<<<<<<<<<<< New process >>>>>>>>>>>")
                            try:
                                handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid)

                                if handle == 0:
                                    print("!!!! FAILED TO OPEN PROCESS HANDLE !!!!")
                                else:
                                    print("<<<<<<<<<<< Patching bgiaa >>>>>>>>>>>")
                                    finaladdr=-1
                                    origbgiaa=b""
                                    try:
                                        addr = 0x400000
                                        off = 0

                                        while True:
                                            mem = win32process.ReadProcessMemory(handle, addr + off, 4096)
                                            bgiaa = mem.find(b"BgIAA")

                                            if bgiaa != -1:
                                                print("<<<<<<<<< Found BgIAA string >>>>>>>>>>")
                                                vqex = windll.kernel32.VirtualProtectEx
                                                vqex.restype = BOOL
                                                vqex.argtypes = [ LONG, LONG, LONG, DWORD, PDWORD ]
                                                dw = DWORD(0)
                                                vqex(int(handle), addr + off + bgiaa, len(PUBLIC_KEY) + 1, 64, PDWORD(dw))
                                                origbgiaa = win32process.ReadProcessMemory(handle, addr + off + bgiaa, len(PUBLIC_KEY.encode("utf-8") + b"\x00"))
                                                win32process.WriteProcessMemory(handle, addr + off + bgiaa, PUBLIC_KEY.encode("utf-8") + b"\x00")
                                                finaladdr = addr + off + bgiaa

                                                vqex(int(handle), addr + off + bgiaa, len(PUBLIC_KEY) + 1, dw, PDWORD(dw))
                                                print("<<<<<<< Patched >>>>>>>>>>")
                                                break

                                            off += 2048
                                    except Exception as e:
                                        print(e)

                                    flow.response.text = SignScript(SCRIPT_PREPEND + "\r\n" + flow.response.text)

                                    seenPids[pid] = [finaladdr, origbgiaa]
                                    win32api.CloseHandle(handle)
                            except:
                                print("!!!! FAILED TO OPEN PROCESS HANDLE !!!!")
            except:
                pass