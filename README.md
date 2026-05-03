# Sub Web Manager

一个轻量级的代理节点订阅管理面板。可以将零散的代理节点链接（如 `hysteria2://...`、`vless://...` 等）集中管理，并生成一个客户端可以直接更新的 Base64 订阅链接。

## 一键安装

在任何一台 Linux 服务器上运行以下命令即可一键安装：

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/liuyue840/sub-web-manager/main/install.sh)
```

**注意：** 安装前请将一键安装脚本中的 `liuyue840` 替换为您自己的 GitHub 用户名。

## 使用说明

1. 访问面板：安装完成后，打开浏览器访问 `http://服务器IP:8123`
2. 添加节点：在面板中直接粘贴您的节点链接，点击“添加”。
3. 复制订阅：面板顶部会生成您的专属 `sub.txt` 链接，直接将其粘贴到 V2rayN, Clash Verge, NekoBox 等代理客户端中即可。

## 特性

- 极简设计，基于 Flask，单文件运行。
- 自动将节点链接 Base64 编码，适配绝大多数代理客户端。
- 包含一键安装脚本，自动配置 systemd 守护进程，开机自启。
