
## ssh-key 生成

    #Enter ls -al ~/.ssh to see if existing SSH keys are present
    ls -al ~/.ssh
    # Lists the files in your .ssh directory, if they exist
    # gen key
    ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# Github 多ssh key导致的权限问题 ：Permission denied (publickey) #

公司用gitlib搭建了git服务器，自己已有github账号，用ssh-keygen分别生成gitlab 的账号和 github账号相对应的两个rsa public key：github_rsa.pub和gitlib_rsa.pub

然后将里面的内容copy到对于网站的SSH-Keys 中，但是都出现了 Permission denied (publickey) （权限问题）

以 github 为例：

    $ ssh -vT git@github.com
    OpenSSH_7.1p2, OpenSSL 1.0.2g  1 Mar 2016
    debug1: Reading configuration data /c/Users/Administrator/.ssh/config
    debug1: Reading configuration data /etc/ssh/ssh_config
    debug1: Connecting to github.com [192.30.253.112] port 22.
    debug1: Connection established.
    debug1: identity file /c/Users/Administrator/.ssh/id_rsa type 1
    debug1: key_load_public: No such file or directory
    debug1: identity file /c/Users/Administrator/.ssh/id_rsa-cert type -1
    debug1: key_load_public: No such file or directory
    debug1: identity file /c/Users/Administrator/.ssh/id_dsa type -1
    debug1: key_load_public: No such file or directory
    debug1: identity file /c/Users/Administrator/.ssh/id_dsa-cert type -1
    debug1: key_load_public: No such file or directory
    debug1: identity file /c/Users/Administrator/.ssh/id_ecdsa type -1
    debug1: key_load_public: No such file or directory
    debug1: identity file /c/Users/Administrator/.ssh/id_ecdsa-cert type -1
    debug1: key_load_public: No such file or directory
    debug1: identity file /c/Users/Administrator/.ssh/id_ed25519 type -1
    debug1: key_load_public: No such file or directory
    debug1: identity file /c/Users/Administrator/.ssh/id_ed25519-cert type -1
    debug1: Enabling compatibility mode for protocol 2.0
    debug1: Local version string SSH-2.0-OpenSSH_7.1
    debug1: Remote protocol version 2.0, remote software version libssh-0.7.0
    debug1: no match: libssh-0.7.0
    debug1: Authenticating to github.com:22 as 'git'
    debug1: SSH2_MSG_KEXINIT sent
    debug1: SSH2_MSG_KEXINIT received
    debug1: kex: server->client chacha20-poly1305@openssh.com <implicit> none
    debug1: kex: client->server chacha20-poly1305@openssh.com <implicit> none
    debug1: expecting SSH2_MSG_KEX_ECDH_REPLY
    debug1: Server host key: ssh-rsa SHA256:asdfnThbg6kXUpJWGl7E1IGOCspdCARLvssdfdsiKwadfxY8
    debug1: Host 'github.com' is known and matches the RSA host key.
    debug1: Found key in /c/Users/Administrator/.ssh/known_hosts:1
    debug1: SSH2_MSG_NEWKEYS sent
    debug1: expecting SSH2_MSG_NEWKEYS
    debug1: SSH2_MSG_NEWKEYS received
    debug1: SSH2_MSG_SERVICE_REQUEST sent
    debug1: SSH2_MSG_SERVICE_ACCEPT received
    debug1: Authentications that can continue: publickey
    debug1: Next authentication method: publickey
    debug1: Offering RSA public key: /c/Users/Administrator/.ssh/id_rsa
    debug1: Authentications that can continue: publickey
    debug1: Trying private key: /c/Users/Administrator/.ssh/id_dsa
    debug1: Trying private key: /c/Users/Administrator/.ssh/id_ecdsa
    debug1: Trying private key: /c/Users/Administrator/.ssh/id_ed25519
    debug1: No more authentication methods to try.
    Permission denied (publickey).

  可以看到本地git 默认指向还是id_rsa,而因为不存在该RSA public key ，所以报出Permission denied(publickey)异常

**解决方案：**

  在~/.ssh 目录中新建config文件，在里面添加下列代码，表明github 的IdentityFile 指向我们自己生成的github_rsa

      Host github.com www.github.com
          IdentityFile ~/.ssh/github_rsa

      Host git.company.com
          IdentityFile ~/.ssh/gitlib_rsa

  再次测试就可以访问了：

    $ ssh -T git@github.com
    Hi ifengkou! You've successfully authenticated, but GitHub does not provide shell access.
