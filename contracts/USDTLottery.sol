pragma solidity ^0.8.0;

// Interface del token USDT en TRC-20
interface IERC20 {
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
}

contract USDTLottery {
    address public owner;
    address public usdtToken; // Dirección del contrato USDT en la red TRC-20
    uint256 public participantCount;
    uint256 public maxParticipants = 150; // Número máximo de participantes por sorteo
    uint256 public participationFee; // Cuota de participación en USDT (ej. 7.0XX USDT con decimales)
    bool public drawOpen;

    struct Participant {
        address wallet;
        uint256 amount;
        bytes32 otpHash;
    }

    mapping(uint256 => Participant[]) public participants; // Lista de participantes por sorteo
    uint256 public currentDrawId;

    event ParticipationRegistered(address indexed participant, uint256 drawId);
    event DrawWinner(uint256 drawId, address winner, uint256 prize);

    constructor(address _usdtToken) {
        owner = msg.sender;
        usdtToken = _usdtToken;
        drawOpen = true;
        currentDrawId = 1;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Solo el propietario puede realizar esta acción");
        _;
    }

    function setParticipationFee(uint256 _fee) external onlyOwner {
        participationFee = _fee;
    }

    function startNewDraw() external onlyOwner {
        require(!drawOpen, "El sorteo actual aún está abierto");
        currentDrawId++;
        drawOpen = true;
    }

    function participate(bytes32 otpHash) external {
        require(drawOpen, "El sorteo está cerrado");
        require(participants[currentDrawId].length < maxParticipants, "Número máximo de participantes alcanzado");
        
        // Transferir el monto exacto al contrato
        require(
            IERC20(usdtToken).transferFrom(msg.sender, address(this), participationFee),
            "Transferencia de USDT fallida"
        );

        // Registrar al participante
        participants[currentDrawId].push(Participant({
            wallet: msg.sender,
            amount: participationFee,
            otpHash: otpHash
        }));

        participantCount++;
        emit ParticipationRegistered(msg.sender, currentDrawId);

        // Cerrar el sorteo si se alcanza el máximo de participantes
        if (participants[currentDrawId].length == maxParticipants) {
            drawOpen = false;
        }
    }

    function executeDraw() external onlyOwner {
        require(!drawOpen, "El sorteo aún está abierto");
        require(participants[currentDrawId].length == maxParticipants, "No hay suficientes participantes");

        // Generar el hash acumulativo
        bytes32 cumulativeHash;
        for (uint256 i = 0; i < participants[currentDrawId].length; i++) {
            cumulativeHash = keccak256(
                abi.encodePacked(cumulativeHash, participants[currentDrawId][i].wallet)
            );
        }

        // Seleccionar al ganador usando el módulo
        uint256 winnerIndex = uint256(cumulativeHash) % maxParticipants;
        address winner = participants[currentDrawId][winnerIndex].wallet;

        // Transferir el premio al ganador
        uint256 prize = IERC20(usdtToken).balanceOf(address(this));
        require(IERC20(usdtToken).transfer(winner, prize), "Fallo al transferir el premio");

        emit DrawWinner(currentDrawId, winner, prize);
    }

    function withdrawFunds(address recipient, uint256 amount) external onlyOwner {
        require(IERC20(usdtToken).transfer(recipient, amount), "Fallo al retirar fondos");
    }

    function getParticipants(uint256 drawId) external view returns (Participant[] memory) {
        return participants[drawId];
    }
}

