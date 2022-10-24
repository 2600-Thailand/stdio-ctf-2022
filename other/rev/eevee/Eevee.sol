// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.6.12;

contract Eevee {
    // STDIO09{0355e3853749700db4e2bd703e214927}
    // forge script Eevee.sol -s "checkFlag(string calldata,string calldata,string calldata,string calldata)" "STDIO09{" "0355" "e3853749700db4e2bd70" "3e214927}"

    function checkFlag0(string calldata inp) pure public returns (bool) {
        return keccak256(bytes(inp)) == keccak256(bytes("STDIO09{"));
    }

    function checkFlag1(string calldata inp) pure public returns (bool) {
        require(bytes(inp).length == 4);
        return keccak256(bytes(inp)) == 0xc3c2d29192c145727c2ac7e1244431dee86ea73be5f7506fcc0139996034141c;
    }

    function checkFlag2(string calldata inp) pure public returns (bool) {
        bytes memory flag2 = new bytes(20);
        flag2[12] = 0x62;
        flag2[0] = 0x65;
        flag2[2] = 0x38;
        flag2[13] = 0x34;
        flag2[4] = 0x33;
        flag2[14] = 0x65;
        flag2[16] = 0x62;
        flag2[5] = 0x37;
        flag2[15] = 0x32;
        flag2[7] = 0x39;
        flag2[8] = 0x37;
        flag2[9] = 0x30;
        flag2[18] = 0x37;
        flag2[10] = 0x30;
        flag2[3] = 0x35;
        flag2[11] = 0x64;
        flag2[19] = 0x30;
        flag2[6] = 0x34;
        flag2[17] = 0x64;
        flag2[1] = 0x33;
        return keccak256(bytes(inp)) == keccak256(flag2);
    }

    function checkFlag3(string calldata inp) pure public returns (bool) {
        bytes memory scrambled = "3791e}242";
        bytes memory inp_str = bytes(inp);
        for (uint i = 0; i < 9; i++) {
            if(inp_str[i] != scrambled[(i * 4) % 9]) {
                return false;
            }
        }
        return true;
    }

    function checkFlag(string calldata inp0, string calldata inp1, string calldata inp2, string calldata inp3) pure public returns (bool) {
        return checkFlag0(inp0) && checkFlag1(inp1) && checkFlag2(inp2) && checkFlag3(inp3);
    }
}